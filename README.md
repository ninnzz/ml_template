# ML Template

This project serves as the basic boilerplate/template for small to intermediate ML apps. Basically I am too lazy to write everything from scratch so I just use this to get all the basic stuff going.

#### Requirements

- `Python 3.10+`
- `Poetry 1.1.12+`

```shell
poetry config virtualenvs.in-project true
poetry install
poetry run python run.py
```

---------------------

### What's included?

- Logging setup
- Config reading
- Data validation using pydantic (with examples)
- Basic project structure
- Some commonly used util functions
    - File operations (s3, local)
    - Callback support (for results)
    - Image handling (for cv projects)
- Pre-commit setup and other things *lazy people* don't want to do.
- Basic unit tests

That's all. What do you expect? 

**It's just a glorified arrangement of folders with some functions for f's sake.**