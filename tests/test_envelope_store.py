import pytest
from pydantic import ValidationError

from panelweaver.schemas.envelope import ErrorClass, StageResult, Status, cache_key, prompt_hash
from panelweaver.store import Store


def test_envelope_roundtrip_through_store(tmp_path):
    store = Store(tmp_path / "pw.sqlite")
    ok = StageResult(stage="ocr", status=Status.OK, confidence=0.93, latency_ms=812)
    bad = StageResult(
        stage="ocr", status=Status.FAILED, error_class=ErrorClass.PROVIDER_ERROR, error="429"
    )
    store.record("demo", ok)
    store.record("demo", bad)
    store.record("other", ok)
    got = store.history("demo", "ocr")
    assert [r.status for r in got] == [Status.OK, Status.FAILED]
    assert got[1].error_class is ErrorClass.PROVIDER_ERROR
    store.close()


def test_envelope_rejects_bad_values():
    with pytest.raises(ValidationError):
        StageResult(stage="x", status=Status.OK, confidence=1.2)
    with pytest.raises(ValidationError):
        StageResult(stage="x", status=Status.OK, surprise=1)


def test_cache_key_is_stable_and_sensitive():
    k = cache_key(["b", "a"], "m1", "prompt v1", {"t": 0})
    assert k == cache_key(["a", "b"], "m1", "prompt v1", {"t": 0})
    assert k != cache_key(["a", "b"], "m1", "prompt v2", {"t": 0})
    assert k != cache_key(["a", "b"], "m2", "prompt v1", {"t": 0})
    assert len(prompt_hash("x")) == 16
