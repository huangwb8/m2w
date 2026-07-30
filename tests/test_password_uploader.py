import importlib.util
import pathlib
import unittest
import sys
import types


def load_uploader_module():
    m2w = types.ModuleType("m2w")
    m2w.upload = types.ModuleType("m2w.upload")
    m2w.update = types.ModuleType("m2w.update")
    m2w.update.find_post = lambda filepath, client: None
    m2w.update.update_post_content = lambda post, filepath, client: True

    sys.modules["m2w"] = m2w
    sys.modules["m2w.upload"] = m2w.upload
    sys.modules["m2w.update"] = m2w.update

    module_path = pathlib.Path(__file__).resolve().parents[1] / "m2w" / "password" / "uploader.py"
    spec = importlib.util.spec_from_file_location("password_uploader_under_test", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PasswordUploaderTests(unittest.TestCase):
    def test_quiet_upload_keeps_success_count(self):
        uploader = load_uploader_module()
        uploaded_posts = []
        uploader.m2w.upload.make_post = lambda filepath, metadata: object()
        uploader.m2w.upload.push_post = lambda post, client: uploaded_posts.append(post)

        uploader.up_password(
            client=object(),
            md_upload=["post.md"],
            md_update=[],
            post_metadata={"category": [], "tag": [], "status": "draft"},
            force_upload=True,
            verbose=False,
        )

        self.assertEqual(len(uploaded_posts), 1)


if __name__ == "__main__":
    unittest.main()
