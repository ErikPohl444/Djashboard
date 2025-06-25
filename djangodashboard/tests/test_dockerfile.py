import subprocess

def test_dockerfile_builds():
    result = subprocess.run(["docker", "build", "-t", "djashboard-test", "."], capture_output=True)
    assert result.returncode == 0