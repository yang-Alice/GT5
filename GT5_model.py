import tensorflow as tf

def _variable_on_cpu(name, shape, initializer):
  with tf.device('/cpu:0'):
    var = tf.get_variable(name, shape, initializer=initializer)
  return var


def _variable_with_weight_decay(name, shape, stddev, wd):
  var = _variable_on_cpu(name, shape,tf.truncated_normal_initializer(stddev=stddev))
  if wd:
    weight_decay = tf.mul(tf.nn.l2_loss(var), wd, name='weight_loss')
    tf.add_to_collection('losses', weight_decay)
return var
	

def inference(images):

	with tf.variable_scope('conv1') as scope:
		kernel=_variable_with_weight_decay('weights',shape=[2,3,3,1,64],stddev=1e-4,wd=0.0)
		conv=tf.nn.conv3d(images, kernel, [1,1,1,1,1], padding='SAME')
