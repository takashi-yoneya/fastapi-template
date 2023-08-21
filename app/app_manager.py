from fastapi import FastAPI


class FastAPIAppManager:
    def __init__(self, root_app: FastAPI) -> None:
        self.app_path_list: list[str] = [""]
        self.root_app: FastAPI = root_app
        self.apps: list[FastAPI] = [root_app]

    def add_app(self, app: FastAPI, path: str) -> None:
        self.apps.append(app)
        if not path.startswith("/"):
            path = f"/{path}"
        else:
            path = path
        self.app_path_list.append(path)
        app.title = f"{self.root_app.title}({path})"
        app.version = self.root_app.version
        app.debug = self.root_app.debug
        self.root_app.mount(path=path, app=app)

    def setup_apps_docs_link(self) -> None:
        """他のAppへのリンクがopenapiに表示されるようにセットする"""
        for app, path in zip(self.apps, self.app_path_list, strict=True):
            app.description = self._make_app_docs_link_html(path)

    def _make_app_docs_link_html(self, current_path: str) -> str:
        # openapiの上部に表示する各Appへのリンクを生成する
        descriptions = [
            f"<a href='{path}/docs'>{path}/docs</a>" if path != current_path else f"{path}/docs"
            for path in self.app_path_list
        ]
        descriptions.insert(0, "Apps link")
        return "<br>".join(descriptions)
