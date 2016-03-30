from generator import *

file = open('../tuning/instances', 'w')
g = Generator()
for i in range(0, 50):
    time_span, omin, omax, dmin, dmax, demand = g.generate_parameters(timespan=5)
    line = " -t="+ str(time_span) + " --offdaymin=" + str(omin) + " --offdaymax=" \
           + str(omax) + " --ondaymin=" + str(dmin)+ " --ondaymax=" + str(dmax)+ " -d=" \
           + str(demand).replace('[', '').replace(']', '') + "\n"
    file.write(line)
for i in range(0,30):
    time_span, omin, omax, dmin, dmax, demand = g.generate_parameters(timespan=7)
    line = " -t=" + str(time_span) + " --offdaymin=" + str(omin) + " --offdaymax=" \
           + str(omax) + " --ondaymin=" + str(dmin)+ " --ondaymax=" + str(dmax)+ " -d=" \
           + str(demand).replace('[', '').replace(']', '') + "\n"
    file.write(line)
for i in range(0, 20):
    time_span, omin, omax, dmin, dmax, demand = g.generate_parameters(timespan=14)
    line = " -t=" + str(time_span) + " --offdaymin=" + str(omin) + " --offdaymax=" \
           + str(omax) + " --ondaymin=" + str(dmin)+ " --ondaymax=" + str(dmax)+ " -d=" \
           + str(demand).replace('[', '').replace(']', '') + "\n"
    file.write(line)
file.close()