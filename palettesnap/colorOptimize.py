###
# Modules
###

# External modules
import numpy as np
import math
from scipy.optimize import minimize, Bounds
import warnings

# Internal modules
from .console import console
from .colorClass import Color, cieColor


###
# Helper Functions
###

# Penalty function
def penalty_function(a, original, weight):
    # Distances
    deviation_penalty = math.sqrt(np.sum((a - original) ** 2))
    # Uniqueness cost
    uniqueness_penalty = np.sum([max(0, 0.1 - abs(a[i] - a[j]))**2 for i in range(len(a)) for j in range(i + 1, len(a))])
    return deviation_penalty + uniqueness_penalty * weight  # Higher means more uniqueness

def no_penalty_function(a, original):
    return 0

# Constraints:
def constraint_1(x):
    def inner_constraint(a):
        return np.abs(a - x) - 33  # Ensure abs(a_i - x) >= 33
    return inner_constraint

def constraint_2(a):
    # Each pair of a_i must differ by at most 20
    n = len(a)
    constraints = []
    for i in range(n):
        for j in range(i + 1, n):
            constraints.append(20 - abs(a[i] - a[j]))
    return np.array(constraints)

###
# Primary Function
###

# Ignore warnings
warnings.filterwarnings("ignore", message="delta_grad == 0.0. Check if the approximated function is linear.")
warnings.filterwarnings("ignore", message="Singular Jacobian matrix. Using SVD decomposition to perform the factorizations.")

def performOptimal(bgLight : int | float, palette : dict[str, Color], weight : int) -> dict[str, Color]:
    '''performs optimization on the lightness of the accent colors'''
    # set up initial values
    lightDict = {key: value for key, value in palette.items() if "bg" not in key}
    lightList = [lightDict[key].cielab[0] for key in lightDict]

    #print(bgLight)
    #print(f"Oklab bg: {palette["bg0"].L}")
    #print(lightList)

    original_values = lightList.copy()
    length = len(original_values)
    bounds = Bounds([0] * length, [100] * length)  # bounds between 0 and 100
    # Constraints
    cons = [{'type': 'ineq', 'fun': constraint_1(bgLight)},
            {'type': 'ineq', 'fun': constraint_2}]
    # extract and print result
    console.log("Optimizing palette colors for good contrast.")
    result = minimize(penalty_function, lightList, args=(original_values, weight), bounds=bounds, constraints=cons, method='trust-constr', options={'disp': False, 'maxiter': 10000})
    if result.success:
        console.log("Optimization [green]succeed[/green].")
        optimized_values = result.x
        #print(optimized_values)
        # return new accent colors
        newLightDict = dict(zip(lightDict.keys(), optimized_values))
        newAccents = dict()
        for key in lightDict:
            newColor = (newLightDict[key], lightDict[key].cielab[1], lightDict[key].cielab[2])
            newAccents[key] = cieColor(newColor)
        return newAccents
    else:
        console.log("Current optimization method [red]failed[/red].")
        console.log("Trying new optimization method.")
        result = minimize(penalty_function, lightList, args=(original_values, weight), bounds=bounds, constraints=cons, method='SLSQP', options={'disp': False, 'maxiter': 10000})
        if result.success:
            console.log("Backup optimization [green]succeed[/green].")
            optimized_values = result.x
            # return new accent colors
            newLightDict = dict(zip(lightDict.keys(), optimized_values))
            newAccents = dict()
            for key in lightDict:
                newColor = (newLightDict[key], lightDict[key].cielab[1], lightDict[key].cielab[2])
                newAccents[key] = cieColor(newColor)
            return newAccents
        else:
            console.log("Backup optimization [red]failed[/red].")
            console.log("Manual optimization process started.")
            console.log("Palette results from manual operation will not be as good as automatic optimization.")
            console.log("Please adjust your settings to prevent manual optimization.")
            console.log("Defining the [b]mode[/b] of your image usually prevents manual optimization.")
            fgLight = palette["fg"].cielab[0]
            if fgLight > bgLight:
                lightThreshold = bgLight + 33
                #lightRange = (lightThreshold, 100)
            else:
                lightThreshold = bgLight - 33
                #lightRange = (0, lightThreshold)
            #optimized_values = [random.uniform(*lightRange) for _ in range(length)]
            optimized_values = [lightThreshold] * length
            #print(optimized_values)
            # return new accent colors
            newLightDict = dict(zip(lightDict.keys(), optimized_values))
            newAccents = dict()
            for key in lightDict:
                newColor = (newLightDict[key], lightDict[key].cielab[1], lightDict[key].cielab[2])
                newAccents[key] = cieColor(newColor)
            return newAccents