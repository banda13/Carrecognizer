from input.data_utils import summ_categories
import input.hasznaltauto.sorter as hasznaltauto_sorter
import input.autotrader.sorter as autotrader_sorter


def sort_into_train_and_test(p_train, p_test, limit):
    input_summ, hasznaltauto_input, autotrader_input = summ_categories(10000)
    for category in input_summ.keys():
        hasznaltauto_count = hasznaltauto_input[category] if hasznaltauto_input[category] < limit else limit
        autotrader_count = limit - hasznaltauto_count

        print("Loading category %s, %d from hasznaltauto, %d from autotrader" % (category, hasznaltauto_count, autotrader_count))

        hasznaltauto_sorter.sort_train_vs_text(p_train, p_test, hasznaltauto_count, [category])
        autotrader_sorter.sort_train_vs_text(p_train, p_test, autotrader_count, [category])

sort_into_train_and_test(0.8, 0.2, 10000)