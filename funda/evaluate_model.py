import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import geopandas as gpd

# © Robin Kratschmayr
class Evaluator(object):
    def __init__(self,base_folder, run_folder, model, model_params):
        self.plot_folder = os.path.join(run_folder, 'plots')
        self.model = model
        self.model_params = model_params
        self.base_folder = base_folder

    def evaluate_model(self, prediction, truth):
        #creating the accuracy and truth, error df
        plt.rcParams["figure.figsize"] = (14,8)
        plt.rcParams['axes.facecolor'] = '#f1f2f1'
        error = pd.DataFrame(prediction,columns=['result'])
        error['truth'] = truth.to_numpy()
        error['result'] = error['result'].astype('int')
        error['accuracy'] = np.absolute((error.result/error.truth)-1)
        error['accuracy_2'] = error['accuracy']

        #some pandas magic to prepare a df for the accuracy plot, could be done easier and more beautiful
        bins_left = [0,0.025,0.05,0.075,0.1,0.125,0.15,0.175,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2]
        bins_save = [0.025,0.05,0.075,0.1,0.125,0.15,0.175,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,8]
        bins_right = [x - 0.0001 for x in bins_save]
        IntervallIndex = pd.IntervalIndex.from_arrays(bins_left,bins_right)
        error_binned = pd.cut(error.accuracy,bins=IntervallIndex)
        error_grouped = error.groupby([error_binned]).count()
        accuracy_plot_data = error_grouped.drop(columns=['result','accuracy','accuracy_2']).reset_index()
        accuracy_plot_data['x_axis'] = accuracy_plot_data.accuracy.apply(lambda x: ("{:3.2f}% - {:3.2f}%".format(x.left*100,x.right*100)))

        #create the accuarcy levels
        acc_levels = [0.025,0.05,0.075,0.1,0.125,0.15,0.175,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.6,0.7,0.8,0.9,1]
        treshold_accuracy_data_list = []
        for acc_level in acc_levels:
            treshold_accuracy_data_list.append(error[error.accuracy < acc_level].shape[0] / error.shape[0])
        acc_level_df = pd.DataFrame(acc_levels, columns=['treshold'])
        acc_level_df['accuracy'] = treshold_accuracy_data_list
        acc_level_df['x_axis'] = acc_level_df.treshold.apply(lambda x: ("{:3.2f}%".format(x*100)))
        
        #create new figure
        evaluation = plt.figure('evaluation')
        x = accuracy_plot_data.truth.reset_index().index.to_list()

        #creating the axes to assign the plots to
        ax1 = plt.subplot(2,2,1)
        ax2 = plt.subplot(2,2,2)
        ax3 = plt.subplot(2,1,2)

        # plot accuracy level plot on axis 1
        y1 = acc_level_df['accuracy'].to_list()
        x3 = acc_level_df['accuracy'].reset_index().index.to_list()
        ax1.bar(x3,y1,color='#656665')
        ax1.set_xlabel('Treshold')
        ax1.set_ylabel('Accuracy')
        xtickslabels = acc_level_df['x_axis'].to_list()
        ticks = acc_level_df['accuracy'].reset_index().index.to_list()
        ax1.set_xticks(ticks)
        ax1.set_xticklabels(xtickslabels, rotation=90)
        

        # plot scatterplot on axis 2
        ax2.scatter(prediction, truth, alpha=0.2)
        ax2.set_xlabel('Predictions')
        ax2.set_ylabel('True Values')
        lims = [0, 3000000]
        ax2.set_xlim(lims)
        ax2.set_ylim(lims)
        ax2.plot(lims, lims)

        #plot accuracy plot on axis 3
        y1 = accuracy_plot_data.truth.to_list()
        ax3.bar(x,y1,color='#656665')
        ax3.set_xlabel('accuracy')
        ax3.set_ylabel('counted')
        xtickslabels = accuracy_plot_data.x_axis.tolist()
        ticks = accuracy_plot_data.reset_index().index.tolist()
        ax3.set_xticks(ticks)
        ax3.set_xticklabels(xtickslabels, rotation=75)

        #add some figure metadata and plot subtitles and save plot to disk
        ax3.set_title("Model accuracy plot")
        ax2.set_title("Predictions vs. reality plot")
        ax1.set_title("Model accuracy on certain treshold")
        text = self.model+" "+ str(self.model_params)
        ax2.text(-2000000, 3700000, text, bbox={'facecolor': 'red', 'alpha': 0.3, 'pad': 10})
        plt.subplots_adjust(wspace=0.15, hspace=0.4)
        plot_name = self.model + "_best.png"
        evaluation.savefig(os.path.join(self.plot_folder,plot_name),bbox_inches='tight')

        return 'evaluated'

    def evaluate_on_map(self, result, truth, test_set_map,accuracy_level):
        #calculate prediction accuracy and group it per municipality
        error = pd.DataFrame(result,columns=['result'])
        error['truth'] = truth.to_numpy()
        error['result'] = error['result'].astype('int')
        error['accuracy'] = np.absolute((error.result/error.truth)-1)
        error['GM_Code'] = test_set_map[['GM2020']].reset_index().drop(columns='index')
        error['treshhold_5'] = error.accuracy.apply(lambda x: 1 if x <=0.05 else 0)
        error['treshhold_10'] = error.accuracy.apply(lambda x: 1 if x <=0.1 else 0)
        number_treshhold = error.groupby('GM_Code').sum().drop(columns=['result','truth','accuracy']).reset_index()
        number_obs = error.groupby('GM_Code').count().drop(columns=['result','accuracy','treshhold_5','treshhold_10']).reset_index()
        geo_df = number_treshhold.merge(number_obs, how="inner", on="GM_Code")
        geo_df['accuracy_5'] = geo_df.treshhold_5 / geo_df.truth
        geo_df['accuracy_10'] = geo_df.treshhold_10 / geo_df.truth
        geo_df['GM_Code'] = geo_df['GM_Code'].astype('int')

        #adding geometrical shapes for each gemeente
        gemeente_boundaries = gpd.read_file(os.path.join(self.base_folder,'data','geometrical','Gemeentegrenzen.gml'))
        gemeente_boundaries['Code'] = gemeente_boundaries['Code'].astype('int')
        final_df = gemeente_boundaries.merge(geo_df, how="left", left_on="Code", right_on="GM_Code") 
        
        #plot accuracy per gemeente as cloropleth and safe it
        p = final_df.plot(column=accuracy_level, figsize = (12,10),legend =True, cmap = 'RdYlGn', vmin=0,vmax=1)
        p.axis('off')
        p.set_title('Accuracy per gemeente with treshhold: {}'.format(accuracy_level))
        p.get_figure().savefig(os.path.join(self.plot_folder,'{}_geo_map_{}.png'.format(self.model,accuracy_level)))
        return 'evaluated'
    