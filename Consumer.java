
package com.pkg;


import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.ConsumerRecords;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.zip.GZIPOutputStream;
import java.time.Duration;
import java.util.Collections;
import java.util.Properties;
public class Consumer {
    private  GZIPOutputStream gos;
    private byte[] buffer = new byte[2046];
    public void gzipFile() throws Exception{

        gos  = new GZIPOutputStream(new FileOutputStream("./test.gz"));
    }
    public void doWork ()throws Exception{
        Properties props = new Properties();
        props.put("bootstrap.servers", "10.0.0.184:9092, 10.0.0.184:9092");
        props.put("ENABLE_AUTO_COMMIT_CONFIG","false");
        props.put("enable.auto.commit","true");
        props.put("max.poll.records",20);
        props.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG, "1000");
        props.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, "30000");
        props.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");
                // group.id，指定了消费者所属群组
        props.put("group.id", "GID1");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");

        KafkaConsumer<String, String> consumer = new KafkaConsumer<String, String>(props);
        consumer.subscribe(Collections.singletonList("CountryCounter"));

        try {
            while (true) {
                // 100 是超时时间（ms），在该时间内 poll 会等待服务器返回数据
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(1));
                // poll 返回一个记录列表。
                // 每条记录都包含了记录所属主题的信息、记录所在分区的信息、记录在分区里的偏移量，以及记录的键值对。

                for (ConsumerRecord<String, String> record : records) {
                    gos.write((record.value()+"\n").getBytes(StandardCharsets.UTF_8));
                   System.out.println("topic="+record.topic()+", partition= "+record.partition()+", offset="+record.offset()+", key="+record.key()+", value="+record.value()+", grp_id"+props.getProperty("group.id"));
                   System.out.println("Batch cnt: "+records.count()+"---rec value:"+record.value());
                }
                    // poll 的数据全部处理完提交
               //
                // consumer.commitSync();
            }
        }catch (Exception e){
            System.out.println("####---->excep");
            gos.finish();
            gos.close();
            throw e;
        }
        finally{
            // 关闭消费者,网络连接和 socket 也会随之关闭，并立即触发一次再均衡
            System.out.println("####---->finally");
            gos.finish();
            gos.close();
            consumer.close();
        }
    }
    public static void main(String[] args) throws Exception{
        // write your code here
    /*    readConfigFile cfgParam = new readConfigFile("/kahome/JAVA_WORKSPACE/projKafkaJavaIdea/src/com/pkg/pgm.cfg");
        cfgParam.printParam();
        String testParam = cfgParam.getParam("test2");
      */
        Consumer cs = new Consumer();
        System.out.println(">>>start doWork");
        cs.gzipFile();
        cs.doWork();
        System.out.println(">>>>+++++\n");
    }
}
