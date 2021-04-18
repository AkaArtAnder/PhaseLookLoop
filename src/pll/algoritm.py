from sympy import Symbol, solve
from random import normalvariate
from math import pi
from time import time

# Parameters
z = Symbol('z')

filter_functions: object

frequency_input_signal: float
frequency_generator: float

start: float
end: float

def main_algoritm(initial_data: dict, self: object) -> dict:
    start = time()

    global filter_functions
    if initial_data['matrix_init'][2] == '1':
        from src.pll.filters import FilterVarA
        filter_functions = FilterVarA(
                                        resistance = initial_data['filter_params'][0],
                                        capacity = initial_data['filter_params'][1],
                                        coefficient_generator = initial_data['filter_params'][2],

        )
    elif initial_data['matrix_init'][2] == '2':
        from src.pll.filters import FilterVarB
        filter_functions = FilterVarB(
                                        resistance = initial_data['filter_params'][0],
                                        capacity = initial_data['filter_params'][1],
                                        coefficient_generator = initial_data['filter_params'][2],
        )
    elif initial_data['matrix_init'][2] == '3':
        from src.pll.filters import FilterVarC
        filter_functions = FilterVarC(
                                        resistance = initial_data['filter_params'][0],
                                        capacity = initial_data['filter_params'][1],
                                        coefficient_generator = initial_data['filter_params'][2],
        )
    
    global frequency_input_signal
    frequency_input_signal = initial_data['freq_input_signal']

    global frequency_generator
    frequency_generator = initial_data['freq_vco_signal']

    # Initial arrays for results
    time_pulse_input_signal = initial_data['input_signal']

    phase_generator_on_period = init_arrays(len(time_pulse_input_signal))
    error_signal = init_arrays(len(time_pulse_input_signal))
    time_pulse_generator = init_arrays(len(time_pulse_input_signal) * 2)
    current_detector = init_arrays(len(time_pulse_input_signal) * 3)
    time_all_pulse = init_arrays(len(time_pulse_input_signal) * 3)
    find_time = init_arrays(len(time_pulse_input_signal) * 2)
    phase = init_arrays(len(time_pulse_input_signal) * 2)

    matrix_x = initial_data['matrix_init'][0]
    matrix_v = initial_data['matrix_init'][1]

    _count = 0
    _count_gen_pulse = 0
    _count_all_pulse = 0
    _count_current = 0
    _count_find = 0

    _count_pulse = 0

    time_pulse_generator[_count_gen_pulse] = 0
    _count_gen_pulse += 1

    current_detector[_count_current] = initial_data['current']
    _count_current += 1

    phase[_count] = initial_data['phase']

    # Algoritm
    while _count < (len(time_pulse_input_signal) - 1):
        self.step += 100/len(time_pulse_input_signal)
        self.progressBar.setValue(self.step)
        
        try:
            period_input_signal = time_pulse_input_signal[_count + 1] - time_pulse_input_signal[_count]
            time_all_pulse[_count_all_pulse] = time_pulse_input_signal[_count]
            _count_all_pulse += 1

            if current_detector[_count_current - 1] >= 0:
                current_detector[_count_current] = 1
                _count_current += 1

                # step 4
                matrix_g = condition_system_filter_and_generator(
                                                                    current=current_detector[_count_current - 1],
                                                                    time_pulse=period_input_signal,
                                                                    condition_system=matrix_x,
                )
                error_signal[_count] = mult_matrixs(matrix_v, matrix_g)
                phase_generator_on_period[_count] = (
                    error_signal[_count] + (2 * pi) * frequency_generator * period_input_signal + phase[_count]
                )

                # step 5
                if phase_generator_on_period[_count] > 2 * pi:
                    # step 7
                    find_time[_count_find] = find_time_pulse_generator(
                                                                current=current_detector[_count_current - 1],
                                                                sym=z,
                                                                condition_system=matrix_x,
                                                                phase=phase[_count],
                                                                time_last_pulse=0,
                                                                matrix_v=matrix_v,
                    )
                    time_pulse_generator[_count_gen_pulse] = time_pulse_input_signal[_count] + find_time[_count_find]
                    _count_pulse += 1
                    time_all_pulse[_count_all_pulse] = time_pulse_generator[_count_gen_pulse]
                    _count_all_pulse += 1
                    matrix_d = condition_system_filter_and_generator(
                                                                        current=current_detector[_count_current - 1],
                                                                        time_pulse=find_time[_count_find],
                                                                        condition_system=matrix_x,
                    )
                    current_detector[_count_current] = 0
                    _count_current += 1

                    _count_find += 1
                    _count_gen_pulse += 1

                    # step 8
                    matrix_g = condition_system_filter_and_generator(
                                                                        current=current_detector[_count_current - 1],
                                                                        time_pulse=(period_input_signal - find_time[_count_find - 1]),
                                                                        condition_system=matrix_d,
                    )
                    phase_generator_on_step_synchronization = (
                        mult_matrixs(matrix_v, matrix_g) + (2 * pi) * frequency_generator * (period_input_signal - find_time[_count_find - 1])
                    )

                    # step 9
                    if phase_generator_on_step_synchronization > 2 * pi:
                        # step 11
                        find_time[_count_find] = (find_time_pulse_generator(
                                                                    current=current_detector[_count_current - 1],
                                                                    sym=z,
                                                                    condition_system=matrix_d,
                                                                    phase=0,
                                                                    time_last_pulse=find_time[_count_find - 1],
                                                                    matrix_v=matrix_v,
                        ))
                        time_pulse_generator[_count_gen_pulse] = time_pulse_input_signal[_count] + find_time[_count_find]
                        _count_pulse += 1
                        time_all_pulse[_count_all_pulse] = time_pulse_generator[_count_gen_pulse]
                        _count_all_pulse += 1
                        matrix_d = condition_system_filter_and_generator(
                                                                            current=current_detector[-1],
                                                                            time_pulse=(find_time[_count_find] - find_time[_count_find - 1]),
                                                                            condition_system=matrix_d,
                        )
                        current_detector[_count_current] = -1
                        _count_current += 1

                        _count_find += 1
                        _count_gen_pulse += 1

                        # step 12
                        while True:
                            matrix_g = condition_system_filter_and_generator(
                                                                                current=current_detector[_count_current - 1],
                                                                                time_pulse=(period_input_signal - find_time[_count_find - 1]),
                                                                                condition_system=matrix_d,
                            )
                            phase_generator_on_step_synchronization = (
                                mult_matrixs(matrix_v, matrix_g) + (2 * pi) * frequency_generator * (period_input_signal - find_time[_count_find - 1])
                            )

                            # step 13
                            if phase_generator_on_step_synchronization < 2 * pi:
                                # step 16
                                matrix_x = matrix_g * 0
                                phase[_count + 1] = abs(phase_generator_on_step_synchronization)
                                _count += 1
                                break
                            else:
                                # step 14
                                find_time[_count_find] = (find_time_pulse_generator(
                                                                                        current=current_detector[_count_current - 1],
                                                                                        sym=z,
                                                                                        condition_system=matrix_d,
                                                                                        phase=0,
                                                                                        time_last_pulse=find_time[_count_find - 1],
                                                                                        matrix_v=matrix_v,
                                ))
                                time_pulse_generator[_count_gen_pulse] = time_pulse_input_signal[_count] + find_time[_count_find]
                                _count_pulse += 1
                                time_all_pulse[_count_all_pulse] = time_pulse_generator[_count_gen_pulse]
                                _count_all_pulse += 1
                                matrix_d = condition_system_filter_and_generator(
                                                                                    current=current_detector[-1],
                                                                                    time_pulse=(find_time[_count_find] - find_time[_count_find - 1]),
                                                                                    condition_system=matrix_d,
                                )
                                current_detector[_count_current] = -1
                                _count_current += 1

                                _count_find += 1
                                _count_gen_pulse += 1
                    # step 10
                    else:
                        matrix_x = matrix_g
                        phase[_count + 1] = abs(phase_generator_on_step_synchronization)
                        _count += 1
                # step 6
                else:
                    matrix_x = matrix_g
                    phase[_count + 1] = phase_generator_on_period[_count]
                    _count += 1
            # step 17
            else:
                current_detector[_count_current] = 0
                _count_current += 1

                matrix_g = condition_system_filter_and_generator(
                                                                    current=current_detector[_count_current - 1],
                                                                    time_pulse=period_input_signal,
                                                                    condition_system=matrix_x,
                )
                error_signal[_count] = mult_matrixs(matrix_v, matrix_g)
                phase_generator_on_period[_count] = (
                        error_signal[_count] + (2 * pi) * frequency_generator * period_input_signal + phase[_count]
                )

                # step 18
                if phase_generator_on_period[_count] > 2 * pi:
                    # step 20
                    find_time[_count_find] = find_time_pulse_generator(
                                                                        current=current_detector[_count_current - 1],
                                                                        sym=z,
                                                                        condition_system=matrix_x,
                                                                        phase=phase[_count],
                                                                        time_last_pulse=0,
                                                                        matrix_v=matrix_v,
                    )
                    time_pulse_generator[_count_gen_pulse] = time_pulse_input_signal[_count] + find_time[_count_find]
                    _count_pulse += 1
                    time_all_pulse[_count_all_pulse] = time_pulse_generator[_count_gen_pulse]
                    _count_all_pulse += 1
                    matrix_d = condition_system_filter_and_generator(
                                                                        current=current_detector[_count_current - 1],
                                                                        time_pulse=find_time[_count_find],
                                                                        condition_system=matrix_x,
                    )
                    current_detector[_count_current] = -1
                    _count_current += 1

                    _count_find += 1
                    _count_gen_pulse += 1

                    # step 21
                    while True:
                        matrix_g = condition_system_filter_and_generator(
                                                                            current=current_detector[_count_current - 1],
                                                                            time_pulse=(period_input_signal - find_time[_count_find - 1]),
                                                                            condition_system=matrix_d,
                        )
                        phase_generator_on_step_synchronization = (
                                mult_matrixs(matrix_v, matrix_g) + (2 * pi) * frequency_generator * (period_input_signal - find_time[_count_find - 1])
                        )

                        # step 22
                        if phase_generator_on_step_synchronization < 2 * pi:
                            # step 25
                            matrix_x = matrix_g
                            phase[_count + 1] = abs(phase_generator_on_step_synchronization)
                            _count += 1
                            break
                        else:
                            # step 23
                            find_time[_count_find] = (find_time_pulse_generator(
                                                                                    current=current_detector[_count_current - 1],
                                                                                    sym=z,
                                                                                    condition_system=matrix_d,
                                                                                    phase=0,
                                                                                    time_last_pulse=find_time[_count_find - 1],
                                                                                    matrix_v=matrix_v,
                            ))
                            time_pulse_generator[_count_gen_pulse] = time_pulse_input_signal[_count] + find_time[_count_find]
                            _count_pulse += 1
                            time_all_pulse[_count_all_pulse] = time_pulse_generator[_count_gen_pulse]
                            _count_all_pulse += 1
                            matrix_d = condition_system_filter_and_generator(
                                                                                current=current_detector[-1],
                                                                                time_pulse=(find_time[_count_find] - find_time[_count_find - 1]),
                                                                                condition_system=matrix_d,
                            )
                            current_detector[_count_current] = -1
                            _count_current += 1

                            _count_find += 1
                            _count_gen_pulse += 1

                # step 19
                else:
                    matrix_x = matrix_g * 0
                    phase[_count + 1] = phase_generator_on_period[_count]
                    _count += 1
        except IndexError:
            print(_count)
            break

    end = time()
    print(f'time finish: ', end-start)
    return {
            'full_phase': phase_generator_on_period[:_count], 'current_detector': current_detector[:_count_current],
            'time_pulse_generator': time_pulse_generator[:_count_gen_pulse], 'time_pulse_input_signal': time_pulse_input_signal[:_count],
            'error_signal': error_signal[:_count], 'time_all_pulse': time_all_pulse[:_count_all_pulse],
    }


# Functions for algoritm
def condition_system_filter_and_generator(**kwargs):
    """
    :param kwargs:
        int: current,
        list: time_pulse,
        matrix: condition_system,
    """
    return filter_functions.exponential(kwargs['time_pulse']) * (
                kwargs['condition_system'] + filter_functions.integral_exponential(kwargs['time_pulse']) * filter_functions.matrix_c * kwargs['current']
    )


def find_time_pulse_generator(**kwargs):
    """
    :param kwargs:
        int:current,
        symbol: sym - time next pulse (find value),
        matrix: condition_system,
        float: phase,
        float: time_last_pulse - time last pulse on period),
        matrix: matrix_v,
    """
    _expression = kwargs['matrix_v'] * (
        filter_functions.symbol_exponential(kwargs['sym'] - kwargs['time_last_pulse']) * (
            kwargs['condition_system'] + filter_functions.symbol_integral_exponential(kwargs['sym'] - kwargs['time_last_pulse']) * filter_functions.matrix_c * kwargs['current']
        )
    )
    _solve_result = solve(
        _expression[0, 0] + (2 * pi) * frequency_generator * (kwargs['sym'] - kwargs['time_last_pulse']) + kwargs['phase'] - (2 * pi), kwargs['sym']
    )
    return select_solve(_solve_result)


def select_solve(solve_result):
    if len(solve_result) == 2:
        if abs(solve_result[0]) < abs(solve_result[1]):
            return abs(solve_result[0])
        else:
            return abs(solve_result[1])
    else:
        return abs(solve_result[0])


def mult_matrixs(matrix_v, matrix_g):
    _mult = matrix_v * matrix_g
    return _mult[0]

def init_arrays(size):
    return [0 for i in range(size)]