"""
Performance tests for llm CLI
"""
import subprocess
import time


def test_help_performance():
    """Test that --help runs in under 200ms"""
    # Run multiple times to get an average
    times = []
    for _ in range(5):
        start = time.time()
        result = subprocess.run(
            ["llm", "--help"],
            capture_output=True,
            text=True,
        )
        elapsed = (time.time() - start) * 1000  # Convert to milliseconds
        times.append(elapsed)

        # Ensure the command succeeded
        assert result.returncode == 0, f"llm --help failed: {result.stderr}"
        assert "Access Large Language Models" in result.stdout

    # Use the median time to avoid outliers
    times.sort()
    median_time = times[len(times) // 2]

    # Assert that median time is under 200ms
    assert median_time < 200, (
        f"llm --help took {median_time:.1f}ms (median of {times}), "
        f"expected < 200ms"
    )

    print(f"✓ llm --help performance: {median_time:.1f}ms (median), all times: {[f'{t:.1f}ms' for t in times]}")


def test_version_performance():
    """Test that --version runs fast (under 200ms)"""
    # --version should not load heavy modules
    times = []
    for _ in range(5):
        start = time.time()
        result = subprocess.run(
            ["llm", "--version"],
            capture_output=True,
            text=True,
        )
        elapsed = (time.time() - start) * 1000  # Convert to milliseconds
        times.append(elapsed)

        # Ensure the command succeeded
        assert result.returncode == 0, f"llm --version failed: {result.stderr}"
        assert "llm, version" in result.stdout

    # Use the median time to avoid outliers
    times.sort()
    median_time = times[len(times) // 2]

    # Assert that median time is under 200ms
    assert median_time < 200, (
        f"llm --version took {median_time:.1f}ms (median of {times}), "
        f"expected < 200ms"
    )

    print(f"✓ llm --version performance: {median_time:.1f}ms (median), all times: {[f'{t:.1f}ms' for t in times]}")


if __name__ == "__main__":
    test_help_performance()
    test_version_performance()
    print("\nAll performance tests passed!")
