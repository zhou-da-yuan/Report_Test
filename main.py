import pytest

if __name__ == "__main__":
    exit_code = pytest.main(['-v', '--color=yes', '-p no:warnings'])
    print(f"Tests finished with exit code: {exit_code}")