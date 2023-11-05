import math
import random
from typing import TypeVar, Callable

TState = TypeVar("TState")


def anneal(
    *,
    initial_state: TState,
    state_cost: Callable[[TState], int],
    tweak_state: Callable[[TState], TState],
    initial_temperature: float,
    iterations_per_temperature: int,
    temperature_decay_factor: float,
) -> TState:
    current_state = initial_state
    current_state_cost = state_cost(current_state)
    optimal_state = initial_state
    optimal_state_cost = state_cost(optimal_state)
    temperature = initial_temperature
    while True:
        current_state_improved = False
        for _ in range(iterations_per_temperature):
            tweaked_state = tweak_state(current_state)
            tweaked_state_cost = state_cost(tweaked_state)
            if tweaked_state_cost < current_state_cost or random.random() < math.exp(
                (current_state_cost - tweaked_state_cost) / temperature
            ):
                if tweaked_state_cost < current_state_cost:
                    current_state_improved = True
                current_state = tweaked_state
                current_state_cost = tweaked_state_cost
            if tweaked_state_cost < optimal_state_cost:
                optimal_state = tweaked_state
                optimal_state_cost = tweaked_state_cost
        if current_state_improved:
            temperature *= temperature_decay_factor
        else:
            break

    return optimal_state


def batch_anneal(
    *,
    initial_states: list[TState],
    state_cost: Callable[[TState], int],
    tweak_state: Callable[[TState], TState],
    initial_temperature: float,
    iterations_per_temperature: int,
    temperature_decay_factor: float,
) -> TState:
    optimal_states = [
        anneal(
            initial_state=initial_state,
            state_cost=state_cost,
            tweak_state=tweak_state,
            initial_temperature=initial_temperature,
            iterations_per_temperature=iterations_per_temperature,
            temperature_decay_factor=temperature_decay_factor,
        )
        for initial_state in initial_states
    ]
    optimal_state_costs = {
        best_state: state_cost(best_state) for best_state in optimal_states
    }
    most_optimal_state = optimal_states[0]
    for optimal_state, optimal_state_cost in optimal_state_costs.items():
        if optimal_state_cost < optimal_state_costs[most_optimal_state]:
            most_optimal_state = optimal_state
    return most_optimal_state
