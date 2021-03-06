import pytest

from django.conf import settings
from django.test import override_settings

from libs.paths.data_paths import get_data_paths, validate_persistence_data
from libs.paths.exceptions import VolumeNotFoundError
from tests.utils import BaseTest


@pytest.mark.paths_mark
class TestDataPaths(BaseTest):
    PERSISTENCE_DATA = {
        'data1': {
            'mountPath': '/data/1',
            'existingClaim': 'test-claim-data-1'
        },
        'data2': {
            'mountPath': '/data/2',
            'hostPath': '/root/data'
        },
        'data3': {
            'store': 'gcs',
            'bucket': 'gs://data-bucket',
            'secret': 'secret-name',
            'secretKey': 'secret-key'
        }
    }

    def test_validate_persistence_data(self):
        assert validate_persistence_data(['path1', 'path2']) == ['path1', 'path2']
        assert validate_persistence_data(None) == settings.PERSISTENCE_DATA.keys()

    def test_get_data_paths_raises_for_unrecognised_paths(self):
        with self.assertRaises(VolumeNotFoundError):
            get_data_paths(['path1', 'path2'])

    @override_settings(PERSISTENCE_DATA=PERSISTENCE_DATA)
    def test_get_data_paths_works_as_expected(self):
        with self.assertRaises(VolumeNotFoundError):
            get_data_paths(['path1', 'path2'])

        assert get_data_paths(['data2']) == {'data2': '/data/2'}
        assert get_data_paths(['data3']) == {'data3': 'gs://data-bucket'}
        assert get_data_paths(['data2', 'data3']) == {'data2': '/data/2',
                                                      'data3': 'gs://data-bucket'}
