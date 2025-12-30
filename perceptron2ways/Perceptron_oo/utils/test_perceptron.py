import unittest
from perceptron import Perceptron
from record import Record
class PreceptronTest(unittest.TestCase):

	def setUp(self):
		"""
        Runs before each test so that each test 
        gets a fresh copy of the object to work with
        """
		self.initial_weights = [-5, 1, 1]
		self.model1 = Perceptron(self.initial_weights)
		self.records = [
			Record((-5, -2.5), 0),
			Record((-7.5, -7.5), 0),
			Record((10, 7.5), 1),
		]
	
	def test_predict1(self):
		for record in self.records:
			reality = self.model1.predict1(record)
			expected = record.actual_label
			self.assertEqual(expected, reality)


	def test_predict_many(self):
		records = [
			Record((-1, -1), 0),
			Record((-5, -2.5), 0),
			Record((5, 10), 1),
			Record((5, 5), 1)
		]
		
		self.model1.predict_many(records)
		expected_labels = [0,0,1,1]

		for index in range(len(records)):
			expected = expected_labels[index]
			reality = records[index].predicted_label
			self.assertEqual(expected, reality)
	
	def test_update_single_performs_calculation_correctly(self):
		# create a model where the actual label (second param) and predicted label are different
		bad_record = Record((-2.5, 12.5), 0)
		bad_record.predicted_label = 1

		self.model1.update_single(bad_record)

		expected_weights = [-6, 3.5, -11.5]
		self.assertEqual(expected_weights, self.model1.weights)

	def test_update_all_ignores_records_with_good_predictions(self):
		records = [
			Record((-1, -1), 0),
			Record((-5, -2.5), 0),
			Record((5, 10), 1),
			Record((5, 5), 1)
		]
		expected = self.initial_weights
		self.model1.predict_many(records)
		self.model1.update_all(records)
		self.assertEqual(expected, self.model1.weights)

	def test_update_all_changes_records_with_bad_predictions(self):
		bad_record = Record((-2.5, 12.5), 0)
		bad_record.predicted_label = 1

		good_record = Record((-1, -1), 0)
		good_record.predicted_label = 0

		records = [bad_record, good_record]

		self.model1.update_all(records)

		expected_weights = [-6, 3.5, -11.5]
		self.assertEqual(expected_weights, self.model1.weights)
	
	def test_score_calculates_correctly_50_50(self):
		bad_record = Record((-2.5, 12.5), 0)
		bad_record.predicted_label = 1

		good_record = Record((-1, -1), 0)
		good_record.predicted_label = 0

		records = [bad_record, good_record]

		expected1 = 0.5
		reality = self.model1.score(records)
		self.assertEqual(expected1, reality)
	
	def test_score_calculates_correctly_thirds(self):
		bad_record = Record((-2.5, 12.5), 0)
		bad_record.predicted_label = 1

		good_record = Record((-1, -1), 0)
		good_record.predicted_label = 0

		records = [bad_record, good_record, good_record]

		expected1 = 2/3
		reality = self.model1.score(records)
		self.assertEqual(expected1, reality)

	def test_train_with_tutorial_data(self):
		records = [
			Record((-1, -1), 0),
			Record((-5, -2.5), 0),
			Record((-7.5, -7.5), 0),
			Record((10, 7.5), 1),
			Record((-2.5, 12.5), 0),
			Record((5, 10), 1),
			Record((5, 5), 1)
		]
		self.model1 = Perceptron(weights=[-5, 1, 1])
		self.model1.train_model(records, 5)

		expected_score = 1.0
		real_score = self.model1.score(records)
		self.assertEqual(expected_score, real_score)

if __name__ == "__main__":
	unittest.main()