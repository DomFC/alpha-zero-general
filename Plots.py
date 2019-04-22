import matplotlib.pyplot as plt


class Plots():
    def __init__(self):
        super().__init__()

    def show_experiment(self, pi_losses, v_losses, nnet_args, main_args):
        plt.figure(num=None, figsize=(11, 8), dpi=80, facecolor='w', edgecolor='k')
        plt.title("Learning curves")
        plt.suptitle('Learning curves', fontsize=16)

        policy_losses_plt = plt.subplot(221)
        policy_losses_plt.set_title("Policy Losses")
        policy_losses_plt.set_xlabel("Iterations")
        policy_losses_plt.set_ylabel("Losses")
        policy_losses_line, = plt.plot(pi_losses, label='policy losses', color='r')
        policy_losses_plt.legend(handles=[policy_losses_line])

        value_losses_plt = plt.subplot(222)
        value_losses_plt.set_title("Value Losses")
        value_losses_plt.set_xlabel("Iterations")
        value_losses_plt.set_ylabel("Losses")
        value_losses_line, = plt.plot(v_losses, label='value losses', color='g')
        value_losses_plt.legend(handles=[value_losses_line])

        data_plt = plt.subplot(223)
        data_plt.get_xaxis().set_visible(False)
        data_plt.get_yaxis().set_visible(False)
        str_plt = (
            '\nLearning rate :  {}'
            '\nEpochs :  {}'
            '\nBatch size : {}'
            '\nnumber of channels : {}'.format(nnet_args.lr, nnet_args.epochs, nnet_args.batch_size, nnet_args.num_channels))
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height
        data_plt.text(0.5 * (left + right), 0.5 * (bottom + top), str_plt,
                      horizontalalignment='center',
                      verticalalignment='center',
                      fontsize=8, color='blue',
                      transform=data_plt.transAxes)

        data_plt = plt.subplot(224)
        data_plt.get_xaxis().set_visible(False)
        data_plt.get_yaxis().set_visible(False)
        str_plt = (
            '\nnumEps :  {}'
            '\ntempThreshold :  {}'
            '\nupdateThreshold :  {}'
            '\nmaxlenOfQueue :  {}'
            '\nnumMCTSSims :  {}'
            '\narenaCompare : {}'.format(main_args.numEps, main_args.tempThreshold, main_args.updateThreshold, main_args.maxlenOfQueue, main_args.numMCTSSims, main_args.arenaCompare))
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height
        data_plt.text(0.5 * (left + right), 0.5 * (bottom + top), str_plt,
                      horizontalalignment='center',
                      verticalalignment='center',
                      fontsize=8, color='blue',
                      transform=data_plt.transAxes)
        plt.show()
