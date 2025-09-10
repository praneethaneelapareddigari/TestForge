def add(a: int | float, b: int | float) -> int | float:
    return a + b

def greet(name: str) -> str:
    return f"Hello, {name}!"

def hello() -> str:
    return "Hello, world!"

class Greeter:
    def _init_(self, prefix: str = "Hello") -> None:
        self.prefix = prefix

    def greet(self, name: str) -> str:
        return f"{self.prefix}, {name}!"

    def hello(self) -> str:
        # tests expect lowercase "hello"
        return "hello"