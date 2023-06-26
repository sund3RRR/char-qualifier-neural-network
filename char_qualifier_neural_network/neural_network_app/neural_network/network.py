import random, numpy, os, csv
from PIL import Image

IMAGE_X = 72
IMAGE_Y = 72

progress = [0]

class neuralNetwork:
    def __init__(self, inodes_c :int, hnodes_c :int, onodes_c :int, learningrate :float):
        self.input_nodes_count = inodes_c
        self.hidden_nodes_count = hnodes_c
        self.output_nodes_count = onodes_c

        self.init_weights()
        weights_dir = os.path.dirname(os.path.abspath(__file__))
        with open(f"{weights_dir}/wih.csv", newline="") as wih_csv:
            csv_reader = csv.reader(wih_csv)
            for row, i in zip(csv_reader, range(0, len(self.wih))):
                self.wih[i] = row
        with open(f"{weights_dir}/who.csv", newline="") as who_csv:
            csv_reader = csv.reader(who_csv)
            for row, i in zip(csv_reader, range(0, len(self.who))):
                self.who[i] = row

        # learning rate
        self.lr = learningrate
        
        # activation function is the sigmoid function
        self.activation_function = Sigmoid


    def init_weights(self) -> None:
        self.wih = numpy.random.normal(0.0, pow(self.input_nodes_count, -0.5), 
            (self.hidden_nodes_count, self.input_nodes_count))
        self.who = numpy.random.normal(0.0, pow(self.hidden_nodes_count, -0.5), 
            (self.output_nodes_count, self.hidden_nodes_count))

    # train the neural network
    def train(self, inputs_list, targets_list) -> None:
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T

        targets = numpy.array(targets_list, ndmin=2).T
        
        # calculate signals into hidden layer
        hidden_inputs = numpy.matmul(self.wih, inputs)

        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        # output layer error is the (target - actual)
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = numpy.dot(self.who.T, output_errors) 
        # update the weights for the links between the hidden and output layers
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)), numpy.transpose(hidden_outputs))
        # update the weights for the links between the input and hidden layers
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), numpy.transpose(inputs))

    
    # query the neural network
    def query(self, inputs_list) -> numpy.ndarray:
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T
        
        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)
        
        return final_outputs

    def dump_weights(self):
        weights_dir = os.path.dirname(os.path.abspath(__file__))
        with open(f"{weights_dir}/wih.csv", 'w', newline='') as wih_csv:
            csv_writer = csv.writer(wih_csv)
            csv_writer.writerows(self.wih)
        with open(f"{weights_dir}/who.csv", 'w', newline='') as who_csv:
            csv_writer = csv.writer(who_csv)
            csv_writer.writerows(self.who)


class TrainDataContainer:
    def __init__(self, target_list, input_list) -> None:
        self.target_list = target_list
        self.input_list = input_list


def Sigmoid(x) -> float:
	return 1.0 / (1.0 + numpy.exp(-x))


def get_input_list(img :Image.Image) -> list[float]:
    '''Returns input list for mnist neural network'''

    pix_val = list(img.getdata())
    for i in range(0, len(pix_val)):
        pix_val[i] = (pix_val[i][0] / 255) * 0.99 + 0.01

    return pix_val


def get_target_list(number :int) -> list[float]:
    '''Returns target list for mnist neural network'''

    target_list = [0.01] * 44
    target_list[number] = 0.99

    return target_list


def get_letter_number(letter):
    alphabet = ["@", "А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т",
        "У", "Ф","Х", "Ц", "Ч", "Ш", "Щ", "Ь", "Ы", "Ъ", "Э", "Ю", "Я"]
    
    return alphabet.index(letter) + 10


def get_train_data(images :list[dict]) -> list[TrainDataContainer]:
    '''Opens dir_name directory, getting pixels from images
    and formatting them to mnist neural network'''
    
    data = []
    
    for image in images:
        input_list = get_input_list(Image.open(image["image"]))

        if image["char"].isdigit():
            letter_number = int(image["char"])
        else:
            letter_number = get_letter_number(image["char"])

        target_list = get_target_list(letter_number)

        data.append(TrainDataContainer(target_list, input_list))

    return data


def start_train(n :neuralNetwork, train_data :list[TrainDataContainer], iter_count :int):
    '''Starts training mnist neural network iter_count times on images in train_data dir'''
    
    n.init_weights()
    train_status = 0
    progress[0] = 0
    for i in range(0, iter_count):
        shuffled_list = train_data.copy()
        random.shuffle(shuffled_list)
        for data_val in shuffled_list:
            n.train(data_val.input_list, data_val.target_list)
        if train_status != int((i + 1)/iter_count * 100):
            train_status = int((i + 1)/iter_count * 100)
            progress[0] = train_status

    n.dump_weights()


def process(image :Image):
    input_list = get_input_list(image)
    return format_ndarray(n.query(input_list))


def format_ndarray(array :numpy.ndarray) -> str:
    '''Formats numpy.ndarray to string representation'''
    result = ""

    for row in array:
        result += str(row[0]) + ' '
    result = result.rstrip(' ')

    return str(result)


input_nodes_count = IMAGE_X * IMAGE_Y
hidden_nodes_count = 800
output_nodes_count = 44

# learning rate
learning_rate = 0.1

# create instance of neural network
n = neuralNetwork(input_nodes_count,hidden_nodes_count,output_nodes_count, learning_rate)