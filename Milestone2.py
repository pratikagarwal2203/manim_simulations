from big_ol_pile_of_manim_imports import *
import os
import pyclbr
import pickle


class EFieldOnCharge(Scene):

    with open('config_elec.txt', 'rb') as conf_file:

        conf = pickle.load(conf_file)

    CONFIG = {
    "plane_kwargs" : {
        "color" : RED_B
        },
    "source_charge_loc" : ORIGIN,
    "point_charge_start_loc" : np.array((conf[0], conf[1], 0)),
    "source_charge_sign" : 1,
    "test_charge_sign" : 1,
    "source_charge_strength" : conf[2],
    "test_charge_strength": conf[3],
    "velocity" : np.array((conf[4], conf[5], 0))

    }

    # CONFIG = {
    #     "plane_kwargs": {
    #         "color": RED_B
    #     },
    #     "source_charge_loc": 1 * LEFT + 1 * UP,
    #     "point_charge_start_loc": -1 * RIGHT - 1 * UP,
    #     "source_charge_sign": 1,
    #     "test_charge_sign": -1,
    #     "source_charge_strength": 0.2,
    #     "test_charge_strength": 0.1,
    #     "velocity": np.array((0.1, 0, 0))
    #
    # }

    def construct(self):

        plane = NumberPlane(**self.plane_kwargs)
        plane.add(plane.get_axis_labels())
        self.add(plane)

        self.source_charge = self.Positron(charge_sign = self.source_charge_sign, radius = self.source_charge_strength).move_to(self.source_charge_loc)
        self.test_charge = self.Positron(charge_sign = self.test_charge_sign, radius = self.test_charge_strength, color = DARK_BLUE, fill_color = DARK_BLUE).move_to(self.point_charge_start_loc)

        self.play(ShowCreation(self.source_charge))
        self.play(ShowCreation(self.test_charge))

        velocity = self.velocity
        current_loc = self.point_charge_start_loc

        for i in range(0, 150):

            acc = self.calc_field(self.source_charge_loc, current_loc) * self.test_charge_sign * self.test_charge_strength
            velocity = velocity + acc
            current_loc = current_loc + velocity

            self.play(Transform(self. test_charge, self.test_charge.shift(velocity)), run_time = 0.05)

        # field = VGroup(*[self.create_vect_field(self.point_charge_start_loc,x*RIGHT+y*UP)
        #     for x in np.arange(-9,9,1)
        #     for y in np.arange(-5,5,1)
        #     ])
        # self.field=field
        # self.source_charge = self.Positron().move_to(self.point_charge_start_loc)
        # self.source_charge.velocity = np.array((1,0,0))
        # self.play(FadeIn(self.source_charge))
        # for i in range(0, 10):
        #     self.play(Transform(self.source_charge, self.source_charge.shift(0.5*RIGHT - 0.125*( 1.5*UP - self.point_charge_start_loc)*UP)))
        # self.play(ShowCreation(field))
        # self.moving_charge()
        # self.continual_update(dt = 1)

    def create_vect_field(self, source_charge, observation_point):
        return Vector(self.calc_field(source_charge, observation_point)).shift(observation_point)

    def calc_field(self, source_point, observation_point):
        x,y,z = observation_point
        Rx,Ry,Rz = source_point
        r = math.sqrt((x-Rx)**2 + (y-Ry)**2 + (z-Rz)**2)

        if r<0.0000001:   #Prevent divide by zero
            efield = np.array((0,0,0))
        else:
            efield = 10*self.source_charge_strength*self.source_charge_sign*(observation_point - source_point)/r**3
        return efield

    class Positron(Circle):
        CONFIG = {
        "radius" : 0.2,
        "stroke_width" : 3,
        "color" : RED,
        "fill_color" : RED,
        "fill_opacity" : 0.9,
        "charge_strength" : 1,
        "charge_sign" : 1
        }
        def __init__(self, **kwargs):
            Circle.__init__(self, **kwargs)

            if self.charge_sign == 1:
                plus = TexMobject("+")
                plus.scale(1.8*self.radius)
                plus.move_to(self)
                self.add(plus)

            elif self.charge_sign == -1:
                minus = TexMobject("-")
                minus.scale(1.8*self.radius)
                minus.move_to(self)
                self.add(minus)



class MagneticForceOnMovingCharge(Scene):

    with open('config_mag.txt', 'rb') as conf_file:

        conf = pickle.load(conf_file)


    CONFIG = {
        "plane_kwargs": {
            "color": RED_B
        },
        "source": conf[0],
        "current_direction": 1,
        "source_charge_loc": np.array((conf[1], conf[2], 0)),
        "point_charge_start_loc": np.array((conf[3], conf[4], 0)),
        "source_charge_sign": 1,
        "test_charge_sign": 1,
        "source_current_strength": conf[5],
        "source_charge_strength": conf[5],
        "test_charge_strength": conf[6],
        "source_velocity": np.array((conf[7], conf[8], 0)),
        "test_velocity": np.array((conf[9], conf[10], 0))

    }

    # CONFIG = {
    #     "plane_kwargs": {
    #         "color": RED_B
    #     },
    #     "source": 'moving charge',
    #     "current_direction": 1,
    #     "source_charge_loc": 1 * LEFT + 1 * UP,
    #     "point_charge_start_loc": -1 * RIGHT - 1 * UP,
    #     "source_charge_sign": 1,
    #     "test_charge_sign": -1,
    #     "source_current_strength": 0.2,
    #     "source_charge_strength": 0.2,
    #     "test_charge_strength": 0.1,
    #     "source_velocity": np.array((0.1, 0, 0)),
    #     "test_velocity": np.array((0.1, 0, 0))
    #
    # }

    #TODO: Write the most general code assuming both electric and magnetic forces and add flags to turn off the influence of a given field

    def construct(self):

        plane = NumberPlane(**self.plane_kwargs)
        plane.add(plane.get_axis_labels())
        self.add(plane)

        if self.source == 'infinite wire':

            line = Line(np.array([-10,0.5,0]), np.array([10,0.5,0]))
            line1 = Line(np.array([-10,0,0]), np.array([10,0,0]))

            self.play(ShowCreation(line), ShowCreation(line1))

            test_charge = self.Positron(charge_sign = self.test_charge_sign,
                                        radius = 2*self.test_charge_strength,
                                        color = DARK_BLUE,
                                        fill_color = DARK_BLUE).move_to(self.point_charge_start_loc)

            self.play(ShowCreation(test_charge))

            points = [np.array([x, 0.25, 0]) for x in np.arange(-100, 100, 1)]

            particles = VGroup(test_charge, *[
                self.Positron(radius=0.2).move_to(point)
                for point in points
            ])

            test_velocity = self.test_velocity
            test_current_loc = self.point_charge_start_loc

            for i in range(0, 60):

                self.play(Transform(particles[1:], particles[1:].shift(self.source_current_strength*self.current_direction*RIGHT)),
                          run_time=0.05)  # for particle in particles)

                test_acc = np.cross(test_velocity, self.calc_field_wire(self.source_current_strength,
                                                self.current_direction, test_current_loc)*self.test_charge_sign*self.test_charge_strength)

                test_velocity = test_velocity + test_acc
                test_current_loc = test_current_loc + test_velocity

                # print(self.calc_field_wire(self.source_current_strength,
                #                                 self.current_direction, test_current_loc))
                # print(test_acc)
                # print(test_velocity)

                self.play(Transform(test_charge, test_charge.shift(test_velocity)), run_time=0.05)

        elif self.source == 'moving charge':

            source_charge = self.Positron(charge_sign = self.source_charge_sign,
                                          radius = 2*self.source_charge_strength).move_to(self.source_charge_loc)

            test_charge = self.Positron(charge_sign = self.test_charge_sign,
                                        radius = 2*self.test_charge_strength,
                                        color = DARK_BLUE,
                                        fill_color = DARK_BLUE).move_to(self.point_charge_start_loc)

            self.play(ShowCreation(source_charge))
            self.play(ShowCreation(test_charge))

            source_velocity = self.source_velocity
            test_velocity = self.test_velocity

            source_current_loc = self.source_charge_loc
            test_current_loc = self.point_charge_start_loc

            for i in range(0, 150):

                test_elec_acc = self.calc_elec_field(source_current_loc,
                                                     test_current_loc) * self.test_charge_sign * self.test_charge_strength
                test_mag_acc = np.cross(test_velocity, self.calc_field_charge(source_current_loc, source_velocity,
                                                                              test_current_loc) * self.test_charge_sign * self.test_charge_strength)

                test_acc = test_elec_acc + test_mag_acc
                test_velocity = test_velocity + test_acc
                test_current_loc = test_current_loc + test_velocity

                self.play(Transform(test_charge, test_charge.shift(test_velocity)), run_time=0.05)

                source_elec_acc = self.calc_elec_field(test_current_loc,
                                                     source_current_loc)*self.test_charge_strength*self.test_charge_sign
                source_mag_acc = np.cross(source_velocity, self.calc_field_charge(test_current_loc, test_velocity,
                                                                              source_current_loc) * self.test_charge_sign * self.test_charge_strength)

                source_acc = source_elec_acc + source_mag_acc
                source_velocity = source_velocity + source_acc
                source_current_loc = source_current_loc + source_velocity

                self.play(Transform(source_charge, source_charge.shift(source_velocity)), run_time=0.05)

                # print(test_acc)

        #
        # field = VGroup(*[self.create_vect_field(self.point_charge_start_loc,x*RIGHT+y*UP)
        #     for x in np.arange(-9,9,1)
        #     for y in np.arange(-5,5,1)
        #     ])
        # self.field=field
        # self.source_charge = self.Positron().move_to(self.point_charge_start_loc)
        # self.source_charge.velocity = np.array((1,0,0))
        # self.play(FadeIn(self.source_charge))
        # for i in range(0, 10):
        #     self.play(Transform(self.source_charge, self.source_charge.shift(0.5*RIGHT - 0.125*( 1.5*UP - self.point_charge_start_loc)*UP)))
        # self.play(ShowCreation(field))
        # self.moving_charge()
        # self.continual_update(dt = 1)

    def create_vect_field(self, source_charge, observation_point):
        return Vector(self.calc_field(source_charge,observation_point)).shift(observation_point)

    def calc_elec_field(self, source_point, observation_point):

        x,y,z = observation_point
        Rx,Ry,Rz = source_point

        r = math.sqrt((x-Rx)**2 + (y-Ry)**2 + (z-Rz)**2)

        efield = np.array((0, 0, 0))
        # if abs(r)<0.0000001:   #Prevent divide by zero
        #     efield = np.array((0,0,0))
        # else:
        #     efield = self.source_charge_strength*self.source_charge_sign*(observation_point - source_point)/r**3
        return efield

    def calc_field_wire(self, current_strength, current_direction, observation_point):

        r = observation_point[1]

        if abs(r)<0.0000001:   #Prevent divide by zero
            mfield = np.array((0,0,0))

        else:
            mfield = np.array((0, 0, current_strength*current_direction/r))

        return mfield

    def calc_field_charge(self, source_point, source_velocity, observation_point):

        x,y,z = observation_point
        Rx,Ry,Rz = source_point

        r = math.sqrt((x-Rx)**2 + (y-Ry)**2 + (z-Rz)**2)

        if abs(r)<0.0000001:   #Prevent divide by zero
            mfield = np.array((0,0,0))
        else:
            mfield = 1000*self.source_charge_strength*self.source_charge_sign*np.cross(source_velocity,
                                                                                  observation_point - source_point)/r**3
        # print(mfield)

        return mfield


    def moving_charge(self):
        numb_charges=3
        # possible_points = [v.get_start() for v in self.field]
        # points = random.sample(possible_points, numb_charges)
        points = [np.array([x, 0.25, 0]) for x in np.arange(-100,100,1)]
        particles = VGroup(self.source_charge, *[
            self.Positron(radius = 0.2).move_to(point)
            for point in points
        ])
        for particle in particles[1:]:
            particle.velocity = np.array((0.2,0,0))
        # self.play(FadeIn(particles[1:]), run_time = 3)
        for i in range(0,10):
            self.play(Transform(particles[1:], particles[1:].shift(0.2*RIGHT)), run_time = 0.05)# for particle in particles)
            self.play(Transform(self.source_charge, self.source_charge.shift(0.2*RIGHT - 0.0125*( 0.2*i)*UP)), run_time = 0.05)
        self.moving_particles = particles
        self.add_foreground_mobjects(self.moving_particles )
        self.play(FadeOut(particles[1:]), run_time = 3)


    class Positron(Circle):
        CONFIG = {
        "radius" : 0.2,
        "stroke_width" : 3,
        "color" : RED,
        "fill_color" : RED,
        "fill_opacity" : 0.75,
        "charge_strength" : 1,
        "charge_sign" : 1
        }
        def __init__(self, **kwargs):
            Circle.__init__(self, **kwargs)

            if self.charge_sign == 1:
                plus = TexMobject("+")
                plus.scale(1.8*self.radius)
                plus.move_to(self)
                self.add(plus)

            elif self.charge_sign == -1:
                minus = TexMobject("-")
                minus.scale(1.8*self.radius)
                minus.move_to(self)
                self.add(minus)
