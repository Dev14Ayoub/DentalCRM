class TestAssertionsMixin:
    def assertDictContainsSubset(self, subset, dictionary, msg=None):
        """
        Check whether dictionary contains all the keys and values in subset.
        Replacement for deprecated assertDictContainsSubset.
        """
        for key, value in subset.items():
            if key not in dictionary or dictionary[key] != value:
                standardMsg = f"{key}: {value} not found in {dictionary}"
                self.fail(self._formatMessage(msg, standardMsg))

    def assertEquals(self, first, second, msg=None):
        """
        Replacement for deprecated assertEquals.
        """
        return self.assertEqual(first, second, msg)
