from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
)

from .....models import (
    Trip,
)
from .abc import (
    InsertionStrategy,
)

if TYPE_CHECKING:
    from typing import (
        Iterable,
        List,
        Union,
    )
    from .....models import (
        Route,
    )

logger = logging.getLogger(__name__)


class IntensiveInsertionStrategy(InsertionStrategy):

    def compute(self, route: Route, trips: Union[Trip, Iterable[Trip]], *args, **kwargs) -> List[Route]:
        if not isinstance(trips, Trip):
            return super().compute(route, trips, *args, **kwargs)
        trip = trips

        routes = list()
        for i in range(len(route.stops) - 1):
            for j in range(i + 1, len(route.stops)):
                conjectured_route = self.compute_one(route, trip, i, j)
                routes.append(conjectured_route)
        return routes
