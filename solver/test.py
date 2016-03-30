from generator import *

g = Generator()
counter = 1
for i in range(0, 50):
    time_span, omin, omax, dmin, dmax, demand = g.generate_parameters(timespan=5)
    f = open('../tuning/instances/instance'+str(time_span)+'_'+str(i+1), "w")
    candidate_id = str(time_span)+str(omin)+str(omax)+str(dmin)+str(dmax)+str(demand).replace(', ', '').replace('[', '').replace(']','')
    line = str(counter)+" "+str(candidate_id)+" -t="+ str(time_span) + " --offdaymin=" + str(omin) + " --offdaymax=" \
           + str(omax) + " --ondaymin=" + str(dmin)+ " --ondaymax=" + str(dmax)+ " -d=" \
           + str(demand).replace('[', '').replace(']', '').replace(' ', '') + "\n"
    f.write(line)
    f.close()
    counter += 1
for i in range(0,30):
    time_span, omin, omax, dmin, dmax, demand = g.generate_parameters(timespan=7)
    f = open('../tuning/instances/instance'+str(time_span)+'_'+str(i+1), "w")
    candidate_id = str(time_span)+str(omin)+str(omax)+str(dmin)+str(dmax)+str(demand).replace(', ', '').replace(' ', '')
    line = str(counter)+" "+str(candidate_id)+" -t="+ str(time_span) + " --offdaymin=" + str(omin) + " --offdaymax=" \
           + str(omax) + " --ondaymin=" + str(dmin)+ " --ondaymax=" + str(dmax)+ " -d=" \
           + str(demand).replace('[', '').replace(']', '').replace(' ', '') + "\n"
    f.write(line)
    f.close()
    counter += 1
for i in range(0, 20):
    time_span, omin, omax, dmin, dmax, demand = g.generate_parameters(timespan=14)
    f = open('../tuning/instances/instance'+str(time_span)+'_'+str(i+1), "w")
    candidate_id = str(time_span)+str(omin)+str(omax)+str(dmin)+str(dmax)+str(demand).replace(', ', '')
    line = str(counter)+" "+str(candidate_id)+" -t="+ str(time_span) + " --offdaymin=" + str(omin) + " --offdaymax=" \
           + str(omax) + " --ondaymin=" + str(dmin)+ " --ondaymax=" + str(dmax)+ " -d=" \
           + str(demand).replace('[', '').replace(']', '').replace(' ', '') + "\n"
    f.write(line)
    f.close()
    counter += 1