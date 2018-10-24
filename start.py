import time
from process import *


if __name__ == '__main__':
    start_time = time.perf_counter()
    print('\n~~~~~~ Application Questionnaire ~~~~~~\n')

    configure_section_mapping()

    process_data_input()

    process_applications()

    end_time = time.perf_counter()

    print('\nTotal Time: ' + time.strftime("%H:%M:%S",  time.gmtime(end_time - start_time)))
    print('\n****** Completed Successfully ******')
