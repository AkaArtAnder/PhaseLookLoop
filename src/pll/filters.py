from sympy import Matrix

class FilterVarA():
    """
    Class description filter first order
    """
    def __init__(self, **kwargs):
        """
        :param kwargs:
            float: resistance,
            list: capacity - one value
            float: coefficient_generator,
        """

        self.resistance = kwargs['resistance']
        self.capacity = kwargs['capacity'][0]
        self.coefficient_generator = kwargs['coefficient_generator']
        self.time_cost = self.resistance * self.capacity

        # Initial matrix for filter
        self.matrix_c = Matrix([
            [self.resistance * self.coefficient_generator / self.time_cost],
            [self.coefficient_generator * self.resistance]
        ])
    
    # Functions for filter
    def exponential(self, time):
        return Matrix([
            [1, 0],
            [time, 1]
        ])


    def integral_exponential(self, time):
        return Matrix([
            [time, 0],
            [-0.5*time**2,  time]
        ])


    def symbol_exponential(self, sym):
        return Matrix([
            [1, 0],
            [sym, 1]
        ])


    def symbol_integral_exponential(self, sym):
        return Matrix([
            [sym, 0],
            [-0.5*sym**2,  sym]
        ])


class FilterVarB():
    """
    Class description filter second order
    """
    def __init__(self, **kwargs):
        """
        :param kwargs:
            float: resistance,
            list: capacity - capacity_first and capacity_second,
            float: coefficient_generator,
        """
        
        self.resistance = kwargs['resistance']
        self.capacity_first = kwargs['capacity'][0]
        self.capacity_second = kwargs['capacity'][1]
        self.coefficient_generator = kwargs['coefficient_generator']
        self.time_cost_first = self.resistance * self.capacity_first
        self.time_cost_second = self.resistance * self.capacity_second

        self.var_a = 1/(self.time_cost_first * self.time_cost_second)
        self.var_b = 1/self.time_cost_first + 1/self.time_cost_second

        # Initial matrix for filter
        self.matrix_c = Matrix([
            [self.resistance * self.coefficient_generator],
            [self.coefficient_generator * self.resistance * self.time_cost_first],
            [0]
        ])
    
    # Functions for filter
    def exponential(self, time):
        return Matrix([
            [1, 0, 0],
            [time, 1, 0],
            [(self.var_a*time**2)/2, self.var_a*time, 1]
        ])


    def integral_exponential(self, time):
        return Matrix([
            [time, 0, 0],
            [-0.5*time**2, time, 0],
            [(self.var_a*time**3)/6, (self.var_a*time**2)/2, time]
        ])


    def symbol_exponential(self, sym):
        return Matrix([
            [1, 0, 0],
            [sym, 1, 0],
            [(self.var_a*sym**2)/2, self.var_a*sym, 1]
        ])


    def symbol_integral_exponential(self, sym):
        return Matrix([
            [sym, 0, 0],
            [-0.5*sym**2, sym, 0],
            [(self.var_a*sym**3)/6, (self.var_a*sym**2)/2, sym]
        ])


class FilterVarC():
    """
    Class description filter second order
    """
    def __init__(self, **kwargs):
        """
        :param kwargs:
            float: resistance,
            list: capacity - capacity_first and capacity_second,
            float: coefficient_generator,
        """
        
        self.resistance = kwargs['resistance']
        self.capacity_first = kwargs['capacity'][0]
        self.capacity_second = kwargs['capacity'][1]
        self.coefficient_generator = kwargs['coefficient_generator']
        self.time_cost_first = self.resistance * self.capacity_first
        self.time_cost_second = self.resistance * self.capacity_second

        self.var_a = 1/(self.time_cost_first * self.time_cost_second)
        self.var_b = 1/self.time_cost_first + 1/self.time_cost_second

        # Initial matrix for filter
        self.matrix_c = Matrix([
            [self.resistance * self.coefficient_generator],
            [0],
            [0]
        ])
    
    # Functions for filter
    def exponential(self, time):
        return Matrix([
            [1, 0, 0],
            [time, 1, 0],
            [(self.var_a*time**2)/2, self.var_a*time, 1]
        ])


    def integral_exponential(self, time):
        return Matrix([
            [time, 0, 0],
            [-0.5*time**2, time, 0],
            [(self.var_a*time**3)/6, (self.var_a*time**2)/2, time]
        ])


    def symbol_exponential(self, sym):
        return Matrix([
            [1, 0, 0],
            [sym, 1, 0],
            [(self.var_a*sym**2)/2, self.var_a*sym, 1]
        ])


    def symbol_integral_exponential(self, sym):
        return Matrix([
            [sym, 0, 0],
            [-0.5*sym**2, sym, 0],
            [(self.var_a*sym**3)/6, (self.var_a*sym**2)/2, sym]
        ])