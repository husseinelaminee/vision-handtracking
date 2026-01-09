from vision.ui.viewer import Viewer

def test_viewer():
    viewer = Viewer(headless=True, timeout=10)
    viewer.run()
