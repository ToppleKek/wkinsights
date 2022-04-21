from wk.structures import Review, Subject
from wk.wkapi import WkAPI
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import sys

def strip_tags(text: str) -> str:
    pattern = re.compile('<[^>]+>')
    return pattern.sub('', text)

def do_koichi_analysis(subject_dataset: list[Subject]) -> None:
    kanji_with_koichi = []
    vocab_with_koichi = []
    data_by_year = {
        'year': [],
        'count': []
    }

    for sub in subject_dataset:
        if sub.type != 'radical' and 'こういち' in strip_tags(sub.get_reading_mnemonic()):
            if not (sub.created_at().year in data_by_year['year']):
                data_by_year['year'].append(sub.created_at().year)
                data_by_year['count'].append(1)
            else:
                data_by_year['count'][data_by_year['year'].index(sub.created_at().year)] += 1

            if sub.type == 'kanji':
                kanji_with_koichi.append(sub)
            if sub.type == 'vocabulary':
                vocab_with_koichi.append(sub)

    print(
        f'KOICHI: There are {len(kanji_with_koichi) + len(vocab_with_koichi)} reading mnemonics that mention こういち. '
        f'{len(kanji_with_koichi)} of these are kanji mnemonics, and {len(vocab_with_koichi)} are vocabulary. '
        '\nThe kanji that mention こういち are:'
    )

    for sub in kanji_with_koichi:
        print(f'{sub.get_characters()}  ', end='')

    print('\nThe vocabulary that mention こういち are:')

    for sub in vocab_with_koichi:
        print(f'{sub.get_characters()}  ', end='')

    print()

    year_df = pd.DataFrame(data_by_year)

    print(year_df)
    plot = year_df.plot(kind='bar', x='year', y='count', legend=False)
    plot.set_xlabel('Year')
    plot.set_ylabel('Number of Items Added')
    plot.get_figure().savefig('koichi_reviews_by_creation_date.png', bbox_inches='tight')

def _reviews_to_dataframe(reviews: list[Review]) -> pd.DataFrame:
    data_dict = {
        'assignment_id': [],
        'created_at': [],
        'ending_srs_stage': [],
        'incorrect_meaning_answers': [],
        'incorrect_reading_answers': [],
        'srs_id': [],
        'starting_srs_stage': [],
        'subject_id': []
    }

    for review in reviews:
        data_dict['assignment_id'].append(review.get_assignment_id())
        data_dict['created_at'].append(review.created_at())
        data_dict['ending_srs_stage'].append(review.get_ending_srs_stage())
        data_dict['incorrect_meaning_answers'].append(review.get_incorrect_meaning_answers())
        data_dict['incorrect_reading_answers'].append(review.get_incorrect_reading_answers())
        data_dict['srs_id'].append(review.get_srs_id())
        data_dict['starting_srs_stage'].append(review.get_starting_srs_stage())
        data_dict['subject_id'].append(review.get_subject_id())

    return pd.DataFrame(data_dict)

def do_review_analysis(api: WkAPI, review_dataset: pd.DataFrame) -> None:
    print(f'REVIEWS: There have been {len(review_dataset)} reviews recorded on this account.')

    # Find the most reivewed subject_id's
    subject_vc = review_dataset['subject_id'].value_counts()

    subject_id_convert = lambda row: api.get_subject(row['index']).get_characters()

    # Create a new index for the series that has the reading characters instead of the numerical ID
    new_index = subject_vc.copy()[:10].reset_index().apply(subject_id_convert, axis=1).values
    fixed_vc = pd.Series(subject_vc[:10])
    fixed_vc.index = new_index

    print(fixed_vc)

    worst_sub = api.get_subject(subject_vc.index[0])

    print(f'The subject {worst_sub.get_characters()} ({worst_sub.get_meanings()[0].meaning}) has been reviewed the most ({subject_vc.iloc[0]} times) ')

    # Plot the top most reviewed (worst) subjects
    top_worst_plot = fixed_vc.plot(kind='bar')
    top_worst_plot.set_xlabel('Subject')
    top_worst_plot.set_ylabel('Number of Reviews')
    top_worst_plot.get_figure().savefig('top_most_reviewed.png', bbox_inches='tight') # TODO: matplotlib does not support CJK by default.

    # Copy of the dataframe that we will modify the index of
    date_indexed_set = review_dataset.copy()
    date_indexed_set = date_indexed_set.set_index('created_at')

    # Add a weekday column to the dataframe
    date_indexed_set.loc[:, 'weekday'] = date_indexed_set.index.weekday

    # Plot the number of incorrect reviews vs. the day of the week
    incorrect_ans_plot = date_indexed_set.groupby('weekday').aggregate(sum).plot(y=['incorrect_meaning_answers', 'incorrect_reading_answers'])
    incorrect_ans_plot.get_figure().savefig('incorrect_reviews_vs_day_of_the_week.png')

    # Plot the number of reviews over time
    review_history_plot = date_indexed_set.groupby([date_indexed_set.index.year, date_indexed_set.index.month]).count().plot(y=['subject_id'])
    review_history_plot.get_figure().savefig('reviews_over_time.png')


def export_csv(dataset: dict, filename: str) -> None:
    pd.DataFrame(dataset).to_csv(filename, index=False, header=True)

def export_df_csv(dataset: pd.DataFrame, filename: str) -> None:
    dataset.to_csv(filename, index=False, header=True)

def main() -> None:
    token = ''
    use_cache = False
    only_cache = False
    for i in range(0, len(sys.argv)):
        if sys.argv[i] == '--token':
            token = sys.argv[i + 1]
            i += 1
        elif sys.argv[i] == '--cache':
            only_cache = True
        elif sys.argv[i] == '--from-cache':
            print('dbg: using cache')
            use_cache = True

    if token == '':
        print('No token provided. Pass a WaniKani APIv2 token with --token <token>')
        exit(1)

    api = WkAPI(token)

    if only_cache:
        print('Caching reviews...')
        export_df_csv(_reviews_to_dataframe(api.get_all_reviews()), 'reviews.csv')
        return

    reviews_df = pd.read_csv('./reviews.csv', parse_dates=['created_at']) if use_cache else _reviews_to_dataframe(api.get_all_reviews())
    do_review_analysis(api, reviews_df)
    do_koichi_analysis(api.get_all_subjects())

if __name__ == "__main__":
    main()
