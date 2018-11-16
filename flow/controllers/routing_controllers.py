"""Contains a list of custom routing controllers."""

from flow.controllers.base_routing_controller import BaseRouter
import random


class ContinuousRouter(BaseRouter):
    """A router used to continuously re-route of the vehicle in a closed loop.

    This class is useful if vehicles are expected to continuously follow the
    same route, and repeat the same route once it reaches its end.
    """

    def choose_route(self, env):
        """Adopt the current edge's route if about to leave the network."""
        if env.vehicles.get_edge(self.veh_id) == \
                env.vehicles.get_route(self.veh_id)[-1]:
            return env.available_routes[env.vehicles.get_edge(self.veh_id)]
        else:
            return None


class MinicityRouter(BaseRouter):
    """A router used to continuously re-route vehicles in minicity scenario.

    This class allows the vehicle to pick a random route at conjunctions.
    """

    def choose_route(self, env):
        vehicles = env.vehicles
        veh_id = self.veh_id
        veh_edge = vehicles.get_edge(veh_id)
        # print("veh_edge", veh_edge)
        veh_route = vehicles.get_route(veh_id)
        # print("veh_route", veh_route)

        veh_next_edge = env.scenario.next_edge(veh_edge, vehicles.get_lane(veh_id))
        # print("veh_next_edge = env.scenario.next_edge()", veh_next_edge)
        not_an_edge = ":"
        no_next = 0

        if len(veh_next_edge) == no_next:
            next_route = None
        elif veh_route[-1] == veh_edge:
            random_route = random.randint(0, len(veh_next_edge) - 1)
            while veh_next_edge[0][0][0] == not_an_edge:
                veh_next_edge = env.scenario.next_edge(veh_next_edge[random_route][0], veh_next_edge[random_route][1])
            next_route = [veh_edge, veh_next_edge[0][0]]
        else:
            next_route = None

        #print("next_route", next_route)
        return next_route


class GridRouter(BaseRouter):
    """A router used to re-route a vehicle within a grid environment."""

    def choose_route(self, env):
        if env.vehicles.get_edge(self.veh_id) == \
                env.vehicles.get_route(self.veh_id)[-1]:
            new_route = [env.vehicles.get_edge(self.veh_id)]
        else:
            new_route = None

        return new_route


class BayBridgeRouter(ContinuousRouter):
    """Assists in choosing routes in select cases for the Bay Bridge scenario.

    Extension to the Continuous Router.
    """

    def choose_route(self, env):
        """See parent class."""
        edge = env.vehicles.get_edge(self.veh_id)
        lane = env.vehicles.get_lane(self.veh_id)

        if edge == "183343422" and lane in [2] \
                or edge == "124952179" and lane in [1, 2]:
            new_route = env.available_routes[edge + "_1"]
        else:
            new_route = super().choose_route(env)

        return new_route
