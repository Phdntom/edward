from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import edward as ed
import numpy as np
import tensorflow as tf

from edward.models import Normal


class test_klqp_class(tf.test.TestCase):

  def test_normalnormal_run(self):
    with self.test_session() as sess:
      x_data = np.array([0.0] * 50, dtype=np.float32)

      mu = Normal(mu=0.0, sigma=1.0)
      x = Normal(mu=tf.ones(50) * mu, sigma=1.0)

      qmu_mu = tf.Variable(tf.random_normal([]))
      qmu_sigma = tf.nn.softplus(tf.Variable(tf.random_normal([])))
      qmu = Normal(mu=qmu_mu, sigma=qmu_sigma)

      # analytic solution: N(mu=0.0, sigma=\sqrt{1/51}=0.140)
      inference = ed.KLqp({mu: qmu}, data={x: x_data})
      inference.run(n_iter=5000)

      self.assertAllClose(qmu.mean().eval(), 0, rtol=1e-2, atol=1e-2)
      self.assertAllClose(qmu.std().eval(), np.sqrt(1 / 51),
                          rtol=1e-2, atol=1e-2)

if __name__ == '__main__':
  ed.set_seed(42)
  tf.test.main()
