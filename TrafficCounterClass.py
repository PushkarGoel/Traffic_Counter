import datetime
import collections

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


def get_dict_file(filename):
    dict_timestamp = {}
    f = open(filename, 'r')
    for line in f.readlines():
        line = line.strip('\n')
        try:
            cur_time = datetime.datetime.strptime(line.split(" ")[0], DATE_FORMAT)

        except ValueError as ve:
            print("The datetime {} is not in correct format! Skipping it".format(line.split(" ")[0]))
            continue

        try:
            count_cars = int(line.split(" ")[1])

        except ValueError as ve:
            print("The count_cars {} is not an integer! Skipping it".format(line.split(" ")[1]))
            continue

        if cur_time in dict_timestamp:
            print("Re entry of same timestamp! Going to skip this")
            continue
        dict_timestamp[cur_time] = count_cars

    f.close()
    return dict_timestamp


def write_file(lines, output_filename):
    outF = open(output_filename, "w")
    for line in lines.split("\n"):
        # write line to output file
        outF.write(line)
        outF.write("\n")
    outF.close()


class TrafficCounter:

    def __init__(self, filename):

        # created a function for parsing file so that any future changes can be easily done
        self.dict_timestamp = get_dict_file(filename)

    def get_total_cars(self):
        return sum(self.dict_timestamp.values())

    def get_dict_daywise(self, dict_timestamp):

        dict_daywise = {}

        for timestamp, count in dict_timestamp.items():

            cur_date = timestamp.date()
            if cur_date in dict_daywise:
                dict_daywise[cur_date] += count
            else:
                dict_daywise[cur_date] = count

        return dict_daywise

    def get_daywise_output(self, dict_daywise):

        result = ""
        for date, count_cars in dict_daywise.items():
            date_f = date.strftime("%Y-%m-%d")
            cur_line = date_f + " " + str(count_cars) + "\n"
            result += cur_line

        return result

    def get_count_daywise(self, day_filename="day_res.txt"):

        dict_daywise = self.get_dict_daywise(self.dict_timestamp)
        output_daywise = self.get_daywise_output(dict_daywise)
        write_file(output_daywise, day_filename)
        return output_daywise

    def get_top_3_hours(self):
        dict_timestamp = self.dict_timestamp
        if len(dict_timestamp) < 3:
            print("There are less than 3 records so can not find top 3 hours")
            return "Can't find top 3"

        # ThisTrafficCounter logic will choose arbitrary values if more than 3 records qualify for top3 hours
        top_hours = sorted(dict_timestamp, key=dict_timestamp.get, reverse=True)[:3]
        result = ""
        for hour in top_hours:
            result += hour.strftime(DATE_FORMAT) + "\n"

        return result

    def get_least_consecutive_hours(self):

        if len(self.dict_timestamp)<3:
            print("As length is less than 3 no 1.5 hour interval can be possibly found")
            return "No contigous interval found"

        dict_timestamp_sorted = collections.OrderedDict(sorted(self.dict_timestamp.items()))

        min_idx = -1
        min_count = float('inf')
        streak = 0

        list_count_cars = []

        for i, (time, cur_count) in enumerate(dict_timestamp_sorted.items()):

            if i == 0:
                last_time = time
                list_count_cars.append(cur_count)
                continue        # print(dict_daywise)

            time_difference = (time - last_time).total_seconds() / 60
            if time_difference == 30:
                streak += 1
                list_count_cars.append(cur_count)

            else:
                streak = 0
                list_count_cars = [cur_count]

            if streak == 2:
                count_cars_interval = sum(list_count_cars)
                # If the count is less than minimum current interval will be chosen
                # It means in the case of multiple intervals with minimum count, the earliest one will be chosen
                if count_cars_interval < min_count:
                    min_count = count_cars_interval
                    min_idx = i - 2

                streak -= 1
                list_count_cars.pop(0)

            last_time = time

        if min_idx == -1:
            print("No contigous time interval found")
            return "No contigous interval found"

        start_timestamp = list(dict_timestamp_sorted)[min_idx]
        end_timestamp = start_timestamp + datetime.timedelta(minutes=90)

        return start_timestamp, end_timestamp

    def get_outputs(self):

        total_cars = self.get_total_cars()
        print("Total cars checked out are ", total_cars)
        output_daywise = self.get_count_daywise()
        print("The daywise care count is \n", output_daywise)
        top_3_hours = self.get_top_3_hours()
        print("The hours with most cars are \n", top_3_hours)
        start_timestamp, end_timestamp = self.get_least_consecutive_hours()
        print("the 1.5 hour contiguous interval with least cars is {} - {}".format(start_timestamp, end_timestamp))


def main():
    filename = "test/sample.txt"
    print("filename is ", filename)
    traffic_obj = TrafficCounter(filename)
    traffic_obj.get_outputs()


if __name__ == '__main__':
    main()
