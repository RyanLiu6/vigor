from typing import List
from utils import CommandRunner


class Compose(CommandRunner):
    def run(self, *args) -> str:
        params = ["docker", "compose"]
        params.extend(args)

        process = super().run(*params, capture_output=True)
        return process.stdout

    def generate_compose_file(self, files: List[str], env: str=None) -> str:
        params = ["config"]

        if env:
            params.append("--env-file")
            params.append(env)

        for file in files:
            params.append("--file")
            params.append(file)

        return self.run(*params)
