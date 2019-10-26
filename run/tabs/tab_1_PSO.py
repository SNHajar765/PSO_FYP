import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

import random
import numpy as np
from oct2py import Oct2Py
from oct2py import octave

octave.addpath("C:/Users/QA/Desktop")

W = 0.5 #inertia
c1 = 0.8 #cognitive weight
c2 = 0.9 #social weight

n_iterations = 10
target_error = 1e-4
n_particles = 30

min_range = 0
max_range = 0

pso_layout = html.Div([
    html.H1('PSO Implementation'),
    html.H3('Enter Minimum Value'),
    dbc.Input(id='min_val', type = 'number', style={'width': '20%'}),
    html.P(id='min-place'),
    # html.H3('Enter Minimum Value'),
    # dbc.Input(id='min_val', type = 'number', style={'width': '20%'}),
    # html.P(id='min-place')
    html.H3('Enter Maximum Value'),
    dbc.Input(id='max_val', type = 'number', style={'width': '20%'}),
    #use this as alternative for output min-val
    html.P(id='max-place'),
    html.Button('Submit',id='button_a', n_clicks= 1),
    html.Div(id='output-disp')
])
 
########################## PSO PROGRAM ######################################################################################################## 
def calc(click,mini,maxi):
    global min_range, max_range
    if click > 1:
        min_range = float(mini)
        max_range = float(maxi)
        

        class Particle():
            def __init__(self):
                #randomizing particle position within permissible range of search spave
                self.position = np.array([random.uniform(min_range,max_range), random.uniform(min_range,max_range), random.uniform(min_range,max_range)])
                #assigning current position to personal best position
                self.pbest_position = self.position
                #'inf' is used to compare solution in algorithms for best solution
                self.pbest_value = float('inf')
                #initializing velocity
                self.velocity = np.array([0,0,0])

            def __return_str__(self):
                return self.position

            #clamp range of particle movement
            def clamp(self):
                rules = [ self.position > min_range, self.position < max_range]
                return rules

            #how each position move to next destination
            def move(self):
                #moving current position
                if (Particle.clamp(self)==bool('true')): 
                    self.position = self.position + self.velocity


        class Space():
            def __init__(self,target, target_error,n_particles):
                self.target = target
                self.target_error = target_error
                self.n_particles = n_particles
                #store data of particles
                self.particles = []
                self.gbest_value = float('inf')
                self.gbest_position = np.array([random.random()*max_range, random.random()*max_range])

            def print_particles(self):
                list_x = []
                list_y = []
                list_z = []
                for particle in self.particles:
                    plotData = particle.__return_str__()
                    X = plotData[0]
                    Y = plotData[1]
                    Z = plotData[2]
                    list_x.append(X)
                    list_y.append(Y)
                    list_z.append(Z)
                df = pd.DataFrame()
                df['X'] = list_x
                df['Y'] = list_y
                df['Z'] = list_z
                export = df.to_json(r'C:\Users\QA\Desktop\PSO_Py\run\tabs\Export_DataFrame.json')

            def fitness(self, particle):
                #pass particle to octave script
                return octave.javelin([particle.position[0],particle.position[1],particle.position[2]])

            def set_pbest(self):
                for particle in self.particles:
                    #assign fitness to fitness_cadidate
                    fitness_cadidate = self.fitness(particle)
                    #if personal value is more than fitness candidate, 
                    if (particle.pbest_value > fitness_cadidate):
                        #update personal best value
                        particle.pbest_value = fitness_cadidate
                        #update personal best position
                        particle.pbest_position = particle.position
                        
            def set_gbest(self):
                for particle in self.particles:
                    #assigning best of the best to best fitness
                    best_fitness_cadidate = self.fitness(particle)
                    if (self.gbest_value > best_fitness_cadidate):
                        self.gbest_value = best_fitness_cadidate
                        self.gbest_position = particle.position
            
            def move_particles(self):
                for particle in self.particles:
                    global W
                    new_velocity = (W*particle.velocity) + (c1*random.random()) * (particle.pbest_position - particle.position) + \
                                    (random.random()*c2) * (self.gbest_position - particle.position)
                    particle.velocity = new_velocity
                    particle.move()
                    #particle.clamp()

        search_space = Space(1,target_error,n_particles) 
        #search_space = Space(1,target_error,n_particles)
        particles_vector = [Particle() for _ in range(search_space.n_particles)]
        search_space.particles = particles_vector
        search_space.print_particles()

        iteration = 0
        while (iteration < n_iterations):
            search_space.set_pbest()
            search_space.set_gbest()

            if(abs(search_space.gbest_value - search_space.target) <= search_space.target_error):
                break

            search_space.move_particles()
            iteration = iteration + 1

        def  return_solution():
            best_value = search_space.gbest_position
            best_solution = octave.javelin(best_value)
            return (best_value, abs(best_solution))

        return u'''Best Solution : {} '''.format(return_solution())


