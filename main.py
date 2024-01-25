import math
import random
import time


class Location:

    def __init__(self):
        self.x = (random.randint(0, 200)) / 10
        self.y = (random.randint(0, 200)) / 10

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def __repr__(self):
        return f"{self.x}, {self.y}"


class Taxi:
    def __init__(self, _id):
        self.loc = Location()
        self.driving = False
        self.id = _id
        self.pickup = False  #with passengers (already picked them up)
        self.ride = []

    def get_x(self):
        return self.loc.get_x()

    def get_y(self):
        return self.loc.get_y()

    def is_driving(self):
        return self.driving

    def get_id(self):
        return self.id

    def get_pickup(self):
        return self.pickup

    def get_ride(self):
        return self.ride

    def set_x(self, x):
        self.loc.set_x(x)

    def set_y(self, y):
        self.loc.set_y(y)

    def set_driving(self, driving):
        self.driving = driving

    def set_pickup(self,pickup):
        self.pickup = pickup

    def set_ride(self, ride):
        self.ride = ride

    def __str__(self):
        x = self.loc.get_x()
        y = self.loc.get_y()
        if not self.driving:
            return f"{x}Km, {y}Km (standing)"
        return f"{x}Km, {y}Km (driving)"

    # def __repr__(self):


class Station:
    def __init__(self):
        self.taxis = []
        self.free = []
        self.rides = []
        for i in range(10):
            taxi = Taxi(i)
            self.taxis.append(taxi)
            self.free.append(i)


    def simulate(self):
        count = 0
        print("Initial taxi locations:")
        for i in range(len(self.taxis)):
            taxi = self.taxis[i]
            print(f"Taxi-{taxi.get_id()+1}: " + str(taxi))
        while True:
            time.sleep(20)
            self.gen_new_ride()
            if self.free != []:
                ride = self.rides.pop(0)
                x = ride[0][0]
                y = ride[0][1]
                closest = self.find_closest(x, y)
                closest.set_driving(True)
                self.free.remove(closest.get_id())
                closest.set_pickup(False)
                closest.set_ride(ride)
            for i in range(len(self.taxis)):
                if self.taxis[i].is_driving():
                    self.advance(self.taxis[i], 0.4)
            count += 20
            print(f"After {count} seconds:")
            print("Order Queue:")
            if(self.rides == []):
                print("Empty")
            else:
                print(self.rides)
            print("Taxi locations:")
            for i in range(len(self.taxis)):
                taxi = self.taxis[i]
                print(f"Taxi-{taxi.get_id() + 1}: " + str(taxi))



    # adds to 'rides' a list of 2 lists [start[x,y], end[x,y]] where the distance is 2Km or below
    def gen_new_ride(self):
        start_x = (random.randint(0, 200)) / 10
        start_y = (random.randint(0, 200)) / 10
        end_x = (random.randint(0, 200)) / 10
        end_y = (random.randint(0, 200)) / 10
        while math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2) > 2:
            end_x = (random.randint(0, 200)) / 10
            end_y = (random.randint(0, 200)) / 10
        # print(f"dist = {math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)}, [start[{start_x},{start_y}], end[{end_x},{end_y}]]")
        self.rides.append([[start_x, start_y], [end_x, end_y]])

    def find_closest(self, x, y):
        if self.free == []:
            raise Exception("No free taxis are left")
        closest = self.taxis[self.free[0]]
        cur_x = closest.get_x()
        cur_y = closest.get_y()
        dist_closest = math.sqrt((cur_x - x)**2 + (cur_y - y)**2)
        # print(dist_closest)
        for i in range(1, len(self.free)):
            cur_x = self.taxis[self.free[i]].get_x()
            cur_y = self.taxis[self.free[i]].get_y()
            dist = math.sqrt((cur_x - x)**2 + (cur_y - y)**2)
            # print(dist)
            if dist < dist_closest:
                closest = self.taxis[self.free[i]]
                dist_closest = dist
        return closest

    def advance(self, taxi, move):
        x = taxi.get_x()
        y = taxi.get_y()
        if not taxi.pickup:  # needs to get to pick up point
            dest_x = taxi.get_ride()[0][0]
            dest_y = taxi.get_ride()[0][1]
        else:
            dest_x = taxi.get_ride()[1][0]
            dest_y = taxi.get_ride()[1][1]
        if dest_x != x:
            if dest_x > x:
                if math.ceil((dest_x - x)*100)/100 < move:
                    taxi.set_x(dest_x)
                    move -= (dest_x - x)
                    move = math.ceil(move*100)/100
                else:
                    temp = math.ceil((x + move)*100)/100
                    taxi.set_x(temp)
                    move = 0
            else:  # dest_x < x
                if math.ceil((x - dest_x)*100)/100 < move:
                    taxi.set_x(dest_x)
                    move -= (x - dest_x)
                    move = math.ceil(move*100)/100
                else:
                    taxi.set_x(math.ceil((x - move)*100)/100)
                    move = 0
        elif dest_y != y and move > 0:
            if dest_y > y:
                if math.ceil((dest_y - y)*100)/100 < move:
                    taxi.set_y(dest_y)
                    move -= (dest_y - y)
                    move = math.ceil(move*100)/100
                else:
                    taxi.set_y(math.ceil((y + move)*100)/100)
                    move = 0
            else:  #dest_y < y
                if math.ceil((y - dest_y)*100)/100 < move:
                    taxi.set_y(dest_y)
                    move -= (y - dest_y)
                    move = math.ceil(move*100)/100
                else:
                    taxi.set_y(math.ceil((y - move)*100)/100)
                    move = 0
        if taxi.get_x() == dest_x and taxi.get_y() == dest_y and taxi.get_pickup():
            taxi.set_driving(False)
            taxi.set_pickup(False)
            taxi.set_ride([])
            self.free.append(taxi.get_id())
            #print(f"Taxi-{taxi.get_id()+1} finished it's ride and free to work again")
        elif taxi.get_x() == dest_x and taxi.get_y() == dest_y and not taxi.get_pickup():
            taxi.set_pickup(True)
            if move > 0:
                self.advance(taxi, move)

def main():
    my_station = Station()
    my_station.simulate()



if __name__ == '__main__':
    main()


