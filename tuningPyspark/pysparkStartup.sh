#!/bin/bash

# pySpark Optimization
# ref: https://blog.cloudera.com/how-to-tune-your-apache-spark-jobs-part-2/
# VM: 2 vCPU, 24 G RAM
# 10 workers: total 200G RAM, 20 vCPU
#    |  20G RAM, 2 vCPU => 1 container of nodemanager can run 2 executor of spark
#       best optimization: (--executor-memory) * (real --num-executors) / total RAM  >=  75 %  => good
# spark executor:
#    |  --num-executors 9999  => stress testing, observing the number of containers in the YARN web UI and modification by accordance
#    |  --executor-cores 1
#    |  --executor-memory 9G  or  8G
#      (20G RAM / 2(one container can run 2 executors))
#      ([10 - 10*0.07] = 9)
# in yarn mode, mem * num_of_executors / total_mem >= 75 % would be mean to be well optimized.


# Setup pyspark to use jupyter lab
export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --port=8888"

# Start pyspark local mode
#pyspark

# Start pyspark local mode
#   modifing the num-executors according to the actually situations after the following setting.
#pyspark --master yarn --deploy-mode cluster \ # error, pyspark can't use cluster mode deploy !!!
pyspark --master yarn --deploy-mode client \
--conf spark.dirver.maxResultSize=2G \  # optional
--driver-memory 1G \
--num-executors 999 \
--executor-cores 1 \
--executor-memory 8G

# Start pyspark local mode with koalas
pyspark --master yarn --deploy-mode client \
--conf spark.sql.execution.arrow.pyspark.enabled=true \
--driver-memory 1G \
--num-executors 999 \
--executor-cores 1 \
--executor-memory 8G

# Start pyspark standalone mode
# standalone mode doesn't need to configure other parameters.
#   for the reason of using all resource by default
pyspark --master "spark://IP_OR_FQDN_OF_MASTER_IN_CLUSTER:7077" --deploy-mode client \
--conf spark.dirver.maxResultSize=2G \
--conf spark.cores.max=1