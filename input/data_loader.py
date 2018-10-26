from input.data_utils import summ_categories
import input.hasznaltauto.sorter as hasznaltauto_sorter
import input.autotrader.sorter as autotrader_sorter


def sort_into_train_and_test(p_train, p_test, limit, max_category):
    input_summ, hasznaltauto_input, autotrader_input = summ_categories(limit)
    counter = 0
    for category in input_summ.keys():
        if category == 'deleted':
            continue
        counter += 1
        if counter < 14:
            print("Category skipped %s" % category)
            continue

        if counter > max_category:
            print("Category limit reached: %d" % max_category)
            break
        hasznaltauto_count = hasznaltauto_input[category] if hasznaltauto_input[category] < limit else limit
        autotrader_count = limit - hasznaltauto_count

        print("Loading category %s, %d from hasznaltauto, %d from autotrader" % (category, hasznaltauto_count, autotrader_count))

        try:
            if hasznaltauto_count > 0:
                hasznaltauto_sorter.sort_train_vs_text(p_train, p_test, hasznaltauto_count, [category])
            if autotrader_count > 0:
                autotrader_sorter.sort_train_vs_text(p_train, p_test, autotrader_count, [category])
            print("Category ready : %d data loaded" % (hasznaltauto_count + autotrader_count))
        except Exception as e:
            print("%s category skipped becasue %s" % (category, str(e)))
