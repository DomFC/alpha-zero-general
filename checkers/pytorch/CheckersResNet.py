import torch
import torch.nn as nn
import torch.nn.functional as F
import sys
sys.path.append('..')


class PolicyHead(nn.Module):

    def __init__(self, input, output, dropout, board_x, board_y):
        super(PolicyHead, self).__init__()
        self.input = input
        self.dropout = dropout
        self.board_x = board_x
        self.board_y = board_y
        self.conv = nn.Conv2d(input, input, 3, stride=1, padding=1)
        self.bn = nn.BatchNorm2d(input)
        self.fc1 = nn.Linear(input*(board_x-2)*(board_y-2), 1024)
        self.fc_bn1 = nn.BatchNorm1d(1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc_bn2 = nn.BatchNorm1d(512)
        self.fc3 = nn.Linear(512, output)

    def forward(self, x):
        x = F.relu(self.bn(self.conv(x)))
        x = x.view(-1, self.input*(self.board_x-2)*(self.board_y-2))
        x = F.dropout(F.relu(self.fc_bn1(self.fc1(x))), p=self.dropout, training=self.training)
        x = F.dropout(F.relu(self.fc_bn2(self.fc2(x))), p=self.dropout, training=self.training)
        policy = F.log_softmax(self.fc3(x), dim=1)
        return policy


class ValueHead(nn.Module):

    def __init__(self, input, output, dropout, board_x, board_y):
        super(ValueHead, self).__init__()
        self.input = input
        self.dropout = dropout
        self.board_x = board_x
        self.board_y = board_y
        self.conv = nn.Conv2d(input, input, 3, stride=1, padding=1)
        self.bn = nn.BatchNorm2d(input)
        self.fc1 = nn.Linear(input*(board_x-2)*(board_y-2), 1024)
        self.fc_bn1 = nn.BatchNorm1d(1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc_bn2 = nn.BatchNorm1d(512)
        self.fc3 = nn.Linear(512, output)
        self.fc4 = nn.Linear(512, 1)

    def forward(self, x):
        x = F.relu(self.bn(self.conv(x)))
        x = x.view(-1, self.input * (self.board_x - 2) * (self.board_y - 2))
        x = F.dropout(F.relu(self.fc_bn1(self.fc1(x))), p=self.dropout, training=self.training)
        x = F.dropout(F.relu(self.fc_bn2(self.fc2(x))), p=self.dropout, training=self.training)
        value = torch.tanh(self.fc4(x))
        return value


class BasicResidualBlock(nn.Module):

    def __init__(self, input, output, stride=1, downsample=None):
        super(BasicResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(input, output, 3, stride, padding=1)
        self.bn1 = nn.BatchNorm2d(output)
        self.conv2 = nn.Conv2d(output, output, 3, stride, padding=1)
        self.bn2 = nn.BatchNorm2d(output)

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = F.relu(self.bn1(out))
        out = self.conv2(out)
        out = self.bn2(out)
        out += residual
        out = F.relu(out)
        return out


class CheckersResNet(nn.Module):

    def __init__(self, game, args):
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args
        self.numberOfResidualBlocks = 20
        super(CheckersResNet, self).__init__()
        self.conv = nn.Conv2d(1, args.num_channels, 3, stride=1, padding=0)
        self.bn = nn.BatchNorm2d(args.num_channels)
        for residual_block in range(self.numberOfResidualBlocks):
            setattr(self, "res{}".format(residual_block), BasicResidualBlock(args.num_channels, args.num_channels))
        self.policy_head = PolicyHead(args.num_channels, self.action_size, self.args.dropout, self.board_x, self.board_y)
        self.value_head = ValueHead(args.num_channels, self.action_size, self.args.dropout, self.board_x, self.board_y)

    def forward(self, x):
        x = x.view(-1, 1, self.board_x, self.board_y)
        x = F.relu(self.bn(self.conv(x)))
        for residual_block in range(self.numberOfResidualBlocks - 1):
             x = getattr(self, "res{}".format(residual_block))(x)
        x = getattr(self, "res{}".format(self.numberOfResidualBlocks - 1))(x)
        policy = self.policy_head(x)
        value = self.value_head(x)
        return policy, value
