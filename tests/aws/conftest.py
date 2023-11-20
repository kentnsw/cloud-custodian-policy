import os
from datetime import datetime, timedelta
from typing import List
from unittest.mock import MagicMock, patch

import pytest
import yaml
from c7n.config import Config
from c7n.policy import PolicyCollection
from c7n.policy import load as policy_load
from c7n.testing import PyTestUtils, reset_session_cache


class CustodianTesting(PyTestUtils):
    def _load_policies(self, path) -> List[PolicyCollection]:
        root_dir = f"{os.path.abspath(__file__)[:-11]}/../../"
        config = {"output_dir": "logs", "account_id": "123456789012"}
        e = Config.empty(**config)
        return policy_load(e, root_dir + path, vars=config)

    def run_policies(self, path) -> list[list]:
        result = []
        for p in self._load_policies(path):
            result.append(p.run())
        return result

    @staticmethod
    def travel(days: int, hours: int = 0, mins: int = 0):
        return datetime.utcnow() + timedelta(days=days, hours=hours, minutes=mins)

    @staticmethod
    def mark_for_op_msg(op, days) -> str:
        return f"Resource does not meet policy: {op}@{CustodianTesting.travel(days).strftime('%Y/%m/%d')}"


@pytest.fixture(scope="function")
def test(request) -> CustodianTesting:
    tester = CustodianTesting(request)
    tester.addCleanup(reset_session_cache)
    return tester


@pytest.fixture(scope="function")
def notify():
    send_sqs = {
        "target": "c7n.actions. notify.Notify.send_sqs",
        "return_value": MagicMock(),
    }
    with patch(**send_sqs) as notify:
        yield notify
