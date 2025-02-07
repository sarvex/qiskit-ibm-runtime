# This code is part of Qiskit.
#
# (C) Copyright IBM 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Program Job REST adapter."""

from typing import Dict

from .base import RestAdapterBase
from ..session import RetrySession


class ProgramJob(RestAdapterBase):
    """Rest adapter for program job related endpoints."""

    URL_MAP = {
        "self": "",
        "results": "/results",
        "cancel": "/cancel",
        "logs": "/logs",
        "interim_results": "/interim_results",
        "metrics": "/metrics",
    }

    def __init__(
        self, session: RetrySession, job_id: str, url_prefix: str = ""
    ) -> None:
        """ProgramJob constructor.

        Args:
            session: Session to be used in the adapter.
            job_id: ID of the program job.
            url_prefix: Prefix to use in the URL.
        """
        super().__init__(session, f"{url_prefix}/jobs/{job_id}")

    def get(self) -> Dict:
        """Return program job information.

        Returns:
            JSON response.
        """
        return self.session.get(self.get_url("self")).json()

    def delete(self) -> None:
        """Delete program job."""
        self.session.delete(self.get_url("self"))

    def interim_results(self) -> str:
        """Return program job interim results.

        Returns:
            Interim results.
        """
        response = self.session.get(self.get_url("interim_results"))
        return response.text

    def results(self) -> str:
        """Return program job results.

        Returns:
            Job results.
        """
        response = self.session.get(self.get_url("results"))
        return response.text

    def cancel(self) -> None:
        """Cancel the job."""
        self.session.post(self.get_url("cancel"))

    def logs(self) -> str:
        """Retrieve job logs.

        Returns:
            Job logs.
        """
        return self.session.get(self.get_url("logs")).text

    def metadata(self) -> str:
        """Retrieve job metadata.

        Returns:
            Job Metadata.
        """
        return self.session.get(self.get_url("metrics")).text
