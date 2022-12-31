import typer
from werkzeug.security import generate_password_hash
import secrets
import os

app = typer.Typer()


@app.command()
def hashpass(plaintext_password: str):
    pwd_hash = generate_password_hash(plaintext_password, method="sha256")
    print(pwd_hash)


@app.command()
def dotenvtemplate(dotenv_path: str):
    env_template_file = os.path.join(os.path.dirname(dotenv_path), "env.template")
    env_template_file_content = []
    try:
        env_file = open(dotenv_path, "r", encoding="utf-8")

        for line in env_file:
            cur_line = line.split("=")[0].strip()
            if cur_line == "":
                continue
            if not cur_line.startswith("#"):
                env_template_file_content.append(cur_line + "=" + "\n")
            else:
                env_template_file_content.append(cur_line + "\n")
        env_file.close()
        try:
            env_template_out_file = open(env_template_file, "w", encoding="utf-8")
            env_template_out_file.writelines(env_template_file_content)
            env_template_out_file.close()
            print(f"File written: {env_template_file}")
        except:
            print(f"File writing failed: {env_template_file}")
    except FileNotFoundError:
        print(f"Not found: {dotenv_path}")


@app.command()
def random32():
    print(secrets.token_urlsafe(32)[:32])


if __name__ == "__main__":
    app()
