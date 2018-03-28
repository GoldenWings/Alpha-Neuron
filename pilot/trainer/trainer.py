from datetime import datetime
import tensorflow as tf
from tensorflow.python.client import timeline
from utility.data_util import *
from utility.data_prep import process_data
from utility.dataset import Dataset
import os
import argparse


class Trainer:

    def __init__(self,
                 data_path,
                 model_file,
                 epochs=50,
                 max_sample_records=500,
                 start_epoch=0,
                 restored_model=False,
                 restored_model_dir=None,
                 tf_timeline=False,
                 show_speed=False):
        self.data_path = data_path
        self.model_file = model_file
        self.n_epochs = int(epochs)
        self.max_sample_records = max_sample_records
        self.tf_timeline = tf_timeline
        if restored_model:
            self.model_dir = restored_model_dir
        else:
            self.tfboard_basedir = os.path.join(self.data_path, 'tf_visual_data', 'runs')
            self.model_dir = mkdir_tfboard_run_dir(self.tfboard_basedir)

        self.results_file = os.path.join(self.model_dir, 'results.txt')
        self.speed_file = os.path.join(self.model_dir, 'speed.txt')
        self.model_checkpoint_dir = os.path.join(self.model_dir,'checkpoints')
        self.saver = tf.train.Saver()
        self.start_epoch = start_epoch
        self.restored_model = restored_model
        mkdir(self.model_checkpoint_dir)

        # Prints batch processing speed, among other things
        self.show_speed = show_speed

    # Used to intentionally overfit and check for basic initialization and learning issues
    def train_one_batch(self, sess, x, y_, accuracy, train_step, train_feed_dict):

        tf.summary.scalar('accuracy', accuracy)
        merged = tf.summary.merge_all()
        sess.run(tf.global_variables_initializer())
        dataset = Dataset(input_file_path=self.data_path, max_sample_records=self.max_sample_records)

        # Not sure what these two lines do
        run_opts = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        run_opts_metadata = tf.RunMetadata()

        train_batches = dataset.get_batches(train=True)
        batch = next(train_batches)
        images, labels = process_data(batch)
        train_feed_dict[x] = images
        train_feed_dict[y_] = labels
        for epoch in range(self.n_epochs):
            train_step.run(feed_dict=train_feed_dict)
            train_summary, train_accuracy = sess.run([merged, accuracy], feed_dict=train_feed_dict,
                                                     options=run_opts, run_metadata=run_opts_metadata)
            test_summary, test_accuracy = sess.run([merged, accuracy], feed_dict=train_feed_dict,
                                                   options=run_opts, run_metadata=run_opts_metadata)
            message = "epoch: {0}, training accuracy: {1}, validation accuracy: {2}"
            print(message.format(epoch, train_accuracy, test_accuracy))

    # This function is agnostic to the model
    def train(self, sess, x, y_, accuracy, train_step, train_feed_dict, test_feed_dict):

        # To view graph: tensorboard
        tf.summary.scalar('accuracy_summary', accuracy)
        merged = tf.summary.merge_all()

        if self.model_file is not None:
            cmd = 'cp {model_file} {archive_path}'
            shell_command(cmd.format(model_file=self.model_file, archive_path=self.model_dir + '/'))

        if not self.restored_model:  # Don't want to erase restored model weights
            sess.run(tf.global_variables_initializer())

        dataset = Dataset(input_file_path=self.data_path, max_sample_records=self.max_sample_records)

        # TODO: Document and understand what RunOptions does
        run_opts = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        run_opts_metadata = tf.RunMetadata()

        train_images, train_labels = process_data(dataset.get_sample(train=True))
        train_feed_dict[x] = train_images
        train_feed_dict[y_] = train_labels
        train_summary, train_accuracy = sess.run([merged, accuracy], feed_dict=train_feed_dict,
                                                 options=run_opts, run_metadata=run_opts_metadata)
        test_images, test_labels = process_data(dataset.get_sample(train=False))
        test_feed_dict[x] = test_images
        test_feed_dict[y_] = test_labels
        test_summary, test_accuracy = sess.run([merged, accuracy], feed_dict=test_feed_dict,
                                               options=run_opts, run_metadata=run_opts_metadata)

        message = "epoch: {0}, training accuracy: {1}, validation accuracy: {2}"
        print(message.format(self.start_epoch, train_accuracy, test_accuracy))

        if self.tf_timeline:  # Used for debugging slow Tensorflow code
            create_tf_timeline(self.model_dir, run_opts_metadata)

        if not self.restored_model:
            with open(self.results_file,'a') as f:
                f.write(message.format(self.start_epoch, train_accuracy, test_accuracy)+'\n')
            self.save_model(sess, epoch=self.start_epoch)

        for epoch in range(self.start_epoch+1, self.start_epoch + self.n_epochs):
            prev_time = datetime.now()
            train_batches = dataset.get_batches(train=True)
            for batch_id, batch in enumerate(train_batches):
                images, labels = process_data(batch)
                train_feed_dict[x] = images
                train_feed_dict[y_] = labels
                sess.run(train_step,feed_dict=train_feed_dict)

                # Track speed to better compare GPUs and CPUs
                now = datetime.now()
                diff_seconds = (now - prev_time).total_seconds()
                if self.show_speed:
                    speed_results = 'batch {batch_id} of {total_batches}, {seconds} seconds'
                    speed_results = speed_results.format(batch_id=batch_id, seconds=diff_seconds,
                                                         total_batches=dataset.batches_per_epoch)
                    with open(self.speed_file, 'a') as f:
                        f.write(speed_results + '\n')
                    print(speed_results)
                prev_time = datetime.now()

            # TODO: Document and understand what RunOptions does
            run_opts = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
            run_opts_metadata = tf.RunMetadata()

            train_images, train_labels = process_data(dataset.get_sample(train=True))
            train_feed_dict[x] = train_images
            train_feed_dict[y_] = train_labels
            train_summary, train_accuracy = sess.run([merged, accuracy], feed_dict=train_feed_dict,
                                                     options=run_opts, run_metadata=run_opts_metadata)
            test_images, test_labels = process_data(dataset.get_sample(train=False))
            test_feed_dict[x] = test_images
            test_feed_dict[y_] = test_labels
            test_summary, test_accuracy = sess.run([merged, accuracy], feed_dict=test_feed_dict,
                                                   options=run_opts, run_metadata=run_opts_metadata)
            print(message.format(epoch, train_accuracy, test_accuracy))
            with open(self.results_file, 'a') as f:
                f.write(message.format(epoch, train_accuracy, test_accuracy)+'\n')

            # Save a model checkpoint after every epoch
            self.save_model(sess,epoch=epoch)

        shell_command('touch ' + self.model_dir + '/SUCCESS')

    def save_model(self,sess,epoch):
        file_path = os.path.join(self.model_checkpoint_dir,'model')
        self.saver.save(sess,file_path,global_step=epoch)
        delete_old_model_backups(checkpoint_dir=self.model_checkpoint_dir)  # Delete all but latest backup to save space


# This is helpful for profiling slow Tensorflow code
def create_tf_timeline(model_dir,run_metadata):
    tl = timeline.Timeline(run_metadata.step_stats)
    ctf = tl.generate_chrome_trace_format()
    timeline_file_path = os.path.join(model_dir,'timeline.json')
    with open(timeline_file_path, 'w') as f:
        f.write(ctf)


def parse_boolean_cli_args(args_value):
    parsed_value = None
    if isinstance(args_value, bool):
        parsed_value = args_value
    elif args_value.lower() in ['y', 'true']:
        parsed_value = True
    else:
        parsed_value = False
    return parsed_value


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--datapath", required=False,
                    help="path to all of the data",
                    default='../Training Data/')
    ap.add_argument("-e", "--epochs", required=False,
                    help="quantity of batch iterations to run",
                    default='50')
    ap.add_argument("-c", "--model_dir", required=False,
                    help="location of checkpoint data",
                    default=None)
    ap.add_argument("-a", "--show_speed", required=False,
                    help="Show speed in seconds",
                    default=False)

    args = vars(ap.parse_args())
    args['show_speed'] = parse_boolean_cli_args(args['show_speed'])
    return args
