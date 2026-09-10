"""Behavioral tests for engine routing; no network, TTS or render needed."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core.preflight import PreflightChecker


class VideoRouting(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.video = self.root / 'output/course/video-1'
        self.video.mkdir(parents=True)
        self.checker = PreflightChecker()
        self.checker.workspace_root = self.root

    def tearDown(self):
        self.temp.cleanup()

    def put(self, relative, text='fixture'):
        path = self.video / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def test_unspecified_engine_asks_even_with_ready_media(self):
        for name in ('images/slide-1.png', 'mp3/mp3-1.mp3', 'mp3/mp3-1.srt'):
            self.put(name)
        report = self.checker.check(str(self.video), for_video=True)
        self.assertEqual(report['status'], 'STATUS_NEED_VIDEO_ENGINE')
        self.assertEqual(report['question'], 'OpenCV hay hyperframes')
        self.assertIsNone(report['engine'])

    def test_hyperframes_accepts_script_without_images_or_audio(self):
        self.put('script.md', '| STT | Nội dung Slide | Prompt tạo ảnh | Voice Script |\n| 1.1 | Tiêu đề | Nền trắng | Xin chào |')
        report = self.checker.check(str(self.video), engine='HyperFrames', for_video=True)
        self.assertEqual(report['status'], 'STATUS_NEED_SCENE_PREPARATION')
        self.assertEqual(report['next_skill'], 'elearning-hyperframes-video')
        self.assertEqual(report['missing'], [])
        self.assertEqual(report['num_images'], 0)
        self.assertIsNone(report['num_voice_sections'])

    def test_hyperframes_does_not_borrow_parent_or_sibling_script(self):
        (self.video.parent / 'script.md').write_text('Parent script', encoding='utf-8')
        sibling = self.video.parent / 'video-2'
        sibling.mkdir()
        (sibling / 'script.md').write_text('Other video', encoding='utf-8')
        report = self.checker.check(str(self.video), engine='hyperframes')
        self.assertEqual(report['status'], 'STATUS_NEED_VIDEO_SCRIPT')
        self.assertIn(str(self.video / 'script.md'), report['missing'][0])

    def test_hyperframes_rejects_empty_script(self):
        self.put('script.md', ' \n')
        self.assertEqual(self.checker.check(str(self.video), engine='hyperframes')['status'],
                         'STATUS_NEED_VIDEO_SCRIPT')

    def test_opencv_keeps_existing_asset_route(self):
        for name in ('images/slide-1.png', 'mp3/mp3-1.mp3', 'mp3/mp3-1.srt'):
            self.put(name)
        report = self.checker.check(str(self.video), engine='OpenCV', for_video=True)
        self.assertEqual(report['status'], 'STATUS_READY_FOR_VIDEO')
        self.assertEqual(report['next_skill'], 'elearning-opencv-video')
        self.assertEqual(report['num_images'], 1)

    def test_inventory_does_not_ask_video_engine_for_documents(self):
        documents = self.root / 'inputs/documents'
        documents.mkdir(parents=True)
        (documents / 'lesson.txt').write_text('Lesson', encoding='utf-8')
        report = self.checker.check(str(self.video))
        self.assertEqual(report['status'], 'STATUS_START_FROM_DOCUMENTS')
        self.assertNotIn('question', report)

    def test_unknown_engine_rejected(self):
        with self.assertRaises(ValueError):
            self.checker.check(str(self.video), engine='random')

    def test_cli_outputs_engine_question_as_json(self):
        run = subprocess.run([sys.executable, '-B', str(ROOT / 'core/preflight.py'),
                              str(self.video), '--stage', 'video', '--json'],
                             capture_output=True, encoding='utf-8')
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['question'], 'OpenCV hay hyperframes')


if __name__ == '__main__':
    unittest.main()
