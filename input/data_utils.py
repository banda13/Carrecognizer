from collections import Counter
import input.autotrader.utils as autotrader
import input.hasznaltauto.utils as hasznaltauto

def summ_categories(limit = 0):
    hasznaltauto_input = hasznaltauto.count_images_per_class()
    autotrader_input = autotrader.count_images_per_class()
    input_summ = Counter(hasznaltauto_input) + Counter(autotrader_input)
    input_summ_with_limit = {}
    for key, value in input_summ.items():
        if int(value) > limit:
            print(key + ": " + str(value))
            input_summ_with_limit[key] = value
    return input_summ_with_limit, hasznaltauto_input, autotrader_input

# summ_categories(10000)