""" Generalized Linear Model with Lasso-regulization """

from importbigdata import *
from matplotlib import pyplot as plt

CSr='rs'

X,y,X_test_box,y_test_box,attributeNames,X_test_names =importbigdata(CSr=CSr,normalize=True, energy_features=True,length_features=True,no_unit_features=True)

#X=np.concatenate((np.ones((X.shape[0],1)),X),1)
#X_test_box = np.hstack((np.ones((X_test_box.shape[0],1)),X_test_box))
#total_attributeNames = [u'Offset']+total_attributenames
N, M= X.shape

#%%



#Create partition for evaluation
K1=5
K2=3
CVouter=cross_validation.KFold(N,K1,shuffle=True)

alphas = np.logspace(-3,-1.5,num=6)

N_gen = len(y)
E_gen= 0 
max_iter=1e4
#%% Finding the optimal model
lassoCV = LassoCV(alphas=alphas,fit_intercept=False,cv=K2,copy_X=True,max_iter=max_iter,n_jobs=-1)
# Finding the generalization error of the optimal model
CV = cross_validation.KFold(N,K1,shuffle = True)

for par_index,test_index in CV:
    X_par = X[par_index,  :]
    X_test= X[test_index,:]
    y_par = y[par_index]
    y_test= y[test_index]
    
    N_test = len(y_test)
    
    lassoCV.fit(X_par,y_par)
    
    y_hat_opt = lassoCV.predict(X_test)
    
    squared_error_vec = np.square(y_test - y_hat_opt)
    E_gen += N_test/N_gen * np.sum(squared_error_vec)/ N_test
    
#%% Optimal model definition
#The weights of the penalized model
alpha  = lassoCV.alpha_
path   = lassoCV.mse_path_
weights= lassoCV.coef_

indices_non_zero = abs(weights) != 0.0 
num_of_non_zero_attributes = np.count_nonzero(weights[:])

X_opt = np.zeros((N,num_of_non_zero_attributes))
X_opt_test_box = np.zeros((X_test_box.shape[0],num_of_non_zero_attributes))
names_opt = []
weights_opt= np.zeros((num_of_non_zero_attributes,1))

inc_opt= 0
for j in range(M):
    if indices_non_zero[j]==True:
        X_opt[:,inc_opt] = X[:,j]
        X_opt_test_box[:,inc_opt] = X_test_box[:,j]
        names_opt.append(attributeNames[j])
        for k in range(len(y)):
            weights_opt[inc_opt] = weights[j]
        inc_opt += 1 


#%% Statistical Measures
prediction_error_test_box = y_test_box.T - lassoCV.predict(X_test_box)
RSS = np.sum(np.square(prediction_error_test_box))
y_hat_test_box = lassoCV.predict(X_test_box)
mean_y_tb = np.average(y_test_box)

prediction_error_tb_percent = np.zeros(len(y_test_box))
for i in range(len(prediction_error_test_box)):
    prediction_error_tb_percent[i] = abs(prediction_error_test_box[i]/y_test_box[i]) * 100
average_error_tb_percent = np.average(prediction_error_tb_percent)
avg_error = np.mean(abs(y_test_box - lassoCV.predict(X_test_box)))
RMSE = np.sqrt(np.sum(np.square(y_hat_test_box - y_test_box))/len(y_test_box))

#%% Crystal Structure Dependent dissimilarity measures

size_CS_vec = int(len(y_test_box)/3)

cs0_nias_error       = np.zeros(size_CS_vec)
cs0_nias_y_true      = np.zeros(size_CS_vec)
cs0_nias_predictions = np.zeros(size_CS_vec)

cs1_zb_error         = np.zeros(size_CS_vec)
cs1_zb_y_true        = np.zeros(size_CS_vec)
cs1_zb_predictions   = np.zeros(size_CS_vec)

cs2_wz_error         = np.zeros(size_CS_vec)
cs2_wz_y_true        = np.zeros(size_CS_vec)
cs2_wz_predictions   = np.zeros(size_CS_vec)


for i in range(size_CS_vec):
    cs0_nias_error[i]       = prediction_error_test_box[i*3+0]
    cs0_nias_y_true[i]      = y_test_box[i*3+0]
    cs0_nias_predictions[i] = y_hat_test_box[i*3+0]
    
    cs1_zb_error[i]         = prediction_error_test_box[i*3+1]
    cs1_zb_y_true[i]        = y_test_box[i*3+1]
    cs1_zb_predictions      = y_hat_test_box[i*3+1]
    
    cs2_wz_error[i]         = prediction_error_test_box[i*3+2]
    cs2_wz_y_true[i]        = y_test_box[i*3+2]
    cs2_wz_predictions      = y_hat_test_box[i*3+2]
    
    

cs0_nias_avg_error = np.average(abs(cs0_nias_error))
cs0_nias_abs_error = abs(cs0_nias_error)
cs0_nias_maxAE     = max(abs(cs0_nias_abs_error))
cs0_nias_RMSE      = np.sqrt(np.sum(np.square(cs0_nias_predictions - cs0_nias_y_true))/size_CS_vec)

cs1_zb_avg_error   = np.average(abs(cs1_zb_error))
cs1_zb_abs_error   = abs(cs1_zb_error)
cs1_zb_maxAE       = max(abs(cs1_zb_abs_error))
cs1_zb_RMSE        = np.sqrt(np.sum(np.square(cs1_zb_predictions -cs1_zb_y_true))/size_CS_vec)

cs2_wz_avg_error   = np.average(abs(cs2_wz_error))
cs2_wz_abs_error   = abs(cs2_wz_error)
cs2_wz_maxAE       = max(abs(cs2_wz_abs_error))
cs2_wz_RMSE        = np.sqrt(np.sum(np.square(cs2_wz_predictions - cs2_wz_y_true))/size_CS_vec)

#%% File saving section
np.savetxt('big_1st_X_opt.csv', X_opt[:,:] ,delimiter=',')                 # Saving the optimal Feature vector
np.savetxt('big_y.csv',y[:],delimiter=',')                                         # y-matrix saved to a .csv file 
np.savetxt('big_1st_weights_opt_2112.csv', weights_opt[:],delimiter=',')      # Weights of the non-zero components
np.savetxt('big_1st_X_opt_test_box_iteration.csv',X_opt_test_box[:,:],delimiter=',') # Saving X_test_box with non-zero attributes corresponding to non-zero weights
np.savetxt('big_y_test_box.csv',y_test_box[:],delimiter=',')
np.savetxt('big_1st_names_opt_iteration.csv', names_opt,delimiter=',',fmt="%s")                    # Names of the non-zero weights
np.savetxt('big_X_test_names.csv',X_test_names,delimiter=',',fmt="%s")                             # Dimer names for plotting
file=open('big_1st_info_iteration.txt','w')                                          # Info about the 1st iteration, num_of_non_zero_features
file.write(str(X_opt.shape[1])+' non-zero features were found. \n Generelization error was: '+str(E_gen)+'\n'+'Optimal alpha was found at '+str(alpha))
file.write('\n The RMSE was found to: '+str(RMSE) + '\n The size of the average error was found to: ' + str(avg_error))
file.write('\n The Residual Sum of Squares was found to: '+str(RSS))
file.write('\n MaxAE was found to: '+str(max(abs(prediction_error_test_box))))
file.write('\n \n \n \n The names for the optimal weights for this iretarations was found to:  \n'+str(names_opt))
file.close()

file=open('big_1st_CS_error_info.txt','w')
file.write('CRYSTAL STRUCTURE DEPENDENT DISSIMILARITY MEASURES: \n \n ')
#NiAs
file.write('NiAs dissimilarity Measures: \n')   
file.write('The average absolute error,  '+str(cs0_nias_avg_error))
file.write('\n The maximal absolute error, maxAE is,  '+str(cs0_nias_maxAE))
file.write('\n The RMSE of the NiAs observations is,  '+str(cs0_nias_RMSE))        
#Zb
file.write('\n \n Zb dissimilarity Measures: \n')   
file.write('The average absolute error,  '+str(cs1_zb_avg_error))
file.write('\n The maximal absolute error, maxAE is,  '+str(cs1_zb_maxAE))
file.write('\n The RMSE of the Zb observations is,  '+str(cs1_zb_RMSE))   
#Wz
file.write('\n \n Wz dissimilarity Measures: \n')   
file.write('The average absolute error,  '+str(cs2_wz_avg_error))
file.write('\n The maximal absolute error, maxAE is,  '+str(cs2_wz_maxAE))
file.write('\n The RMSE of the Wz observations is,  '+str(cs2_wz_RMSE))
file.close()
                                                        
   #%% 
#Plot and save .csv file

file=open('big_1st_lassoCV_all_{0}.csv'.format(CSr),'w')
file.write('i,names,p1,t1,p2,t2,p3,t3,error1,error2,error3,hit1,hit2,hit3\n')
f= figure(); f.hold(True)
hit_miss_total=0
for i in range(0,len(y_test_box),3):
    hit_or_miss=[0,0,0]
    for j in range(len(cs)):
        #plot(i,multilassoCV.predict(X_test_box[i,:])[0,j],'bs',i,y_test_box[i,j],'r^') 
    
        if (lassoCV.predict(X_test_box[i+j,:])[0]<0 and y_test_box[i+j]<0) or (lassoCV.predict(X_test_box[i+j,:])[0]>0 and y_test_box[i+j]>0):
            hit_or_miss[j] =1
            hit_miss_total +=1
    file.write(str(int(i/3))+','
               +str(X_test_names[i])
               +','+str(lassoCV.predict(X_test_box[i,:])[0])
               +','+str(y_test_box[i])
               +','+str(lassoCV.predict(X_test_box[i+1,:])[0])
               +','+str(y_test_box[i+1])
               +','+str(lassoCV.predict(X_test_box[i+2,:])[0])
               +','+str(y_test_box[i+2])
               +','+str(prediction_error_test_box[i])
               +','+str(prediction_error_test_box[1+i])
               +','+str(prediction_error_test_box[2+i])
               +','+str(hit_or_miss[0])
               +','+str(hit_or_miss[1])
               +','+str(hit_or_miss[2])
               +'\n')

plt.xticks(range(len(y_test_box)),X_test_names)
xlabel('Dimer')
ylabel('Heat of formation')    
legend(['Predicted value', 'Target value' ])
savefig('prediction{0}.png'.format(K1))
file.close()
show()

print("The generalization error of the selected optimal is: %.4f"%E_gen)
print("The RMSE of the optimal model tested on the secret box data is: %.4f"%RMSE)
print('Optimal alpha was found at '+str(alpha))
print('The average error on the test box is '+str(avg_error))
print('The correct sign was predicted '+str(hit_miss_total)+' times out of '+str(len(y_test_box))+ ' times')
print('The correct sign was predicted '+str(float(hit_miss_total)/len(y_test_box) *100)+' percent of the time ')





































