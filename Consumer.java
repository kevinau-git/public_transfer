    
    package com.pkg;
    
    
    import org.apache.kafka.clients.consumer.ConsumerConfig;
    import org.apache.kafka.clients.consumer.ConsumerRecord;
    import org.apache.kafka.clients.consumer.KafkaConsumer;
    import org.apache.kafka.clients.consumer.ConsumerRecords;
    
    import sun.misc.Signal;
    import sun.misc.SignalHandler;
    
    import java.io.*;
    import java.util.*;
    import java.util.zip.GZIPOutputStream;
    import java.time.Duration;
    
    public class Consumer implements SignalHandler {
        private BufferedWriter bf_writer = null;
        private Properties props = null;
        private long p_split_cnt = 0;
        private long p_RuntimeSec = 0;
    
        //private byte[] buffer = new byte[2046];
        public Consumer (String args[]) throws Exception{
            props = new Properties();
            props.load(new FileInputStream("./kafka_conf.properties"));
            props.load(new FileInputStream("./kafka_conf_job.properties"));
            props.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG, "1000");
            props.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, "30000");
            props.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");
            System.out.println(">> Param <<");
    
            p_split_cnt = Integer.parseInt(props.getProperty("userparam.split.filecnt","0"));
            p_RuntimeSec = Integer.parseInt(props.getProperty("userparam.runtime.sec","0"));
            for (String key: props.stringPropertyNames()){
                System.out.println(key+"---"+props.getProperty(key));
    
            }
            System.out.println( p_split_cnt);
        }
        public void handle (Signal signalName) {
            System.out.println("exit---->"+signalName);
            try {
                this.bf_writer.flush();
                this.bf_writer.close();
            }catch (Exception e){
                e.printStackTrace();
            }
        }
        public void crtGzipFile(String inFileName) throws Exception{
            GZIPOutputStream gos  = new GZIPOutputStream(new FileOutputStream(inFileName));
            this.bf_writer = new BufferedWriter(new OutputStreamWriter(gos,"UTF-8"));
        }
        public void closeGzipFIle() throws Exception{
            this.bf_writer.flush();
            this.bf_writer.close();
        };
        public void doWork ()throws Exception{
            int fileSeq = 0; //---Split gz file row number
            long rCnt = 0; //----- Count current offset
            long sTime = System.currentTimeMillis();
            long eTime = 0;
    
            KafkaConsumer<String, String> consumer = new KafkaConsumer<String, String>(props);
            List lst = new ArrayList<String>();
            lst.add(props.getProperty("userparam.kafka_topic"));
            consumer.subscribe(lst);
           // consumer.subscribe(Collectns.singletonList("1"));
    
            try {
                this.crtGzipFile("./test"+String.valueOf(fileSeq)+".gz");
    
                while (true) {
               // for (int i =0;i<100 ;i++){
                    // 100 是超时时间（ms），在该时间内 poll 会等待服务器返回数据
                    ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(5));
                    // poll 返回一个记录列表。
                    // 每条记录都包含了记录所属主题的信息、记录所在分区的信息、记录在分区里的偏移量，以及记录的键值对。
                    for (ConsumerRecord<String, String> record : records) {
                        rCnt++;
                       // gos.write((record.value()+"\n").getBytes(StandardCharsets.UTF_8));
                        bf_writer.append(record.value());
                        bf_writer.newLine();
                        System.out.println("topic="+record.topic()+", partition= "+record.partition()+", offset="+record.offset()+", key="+record.key()+", value="+record.value()+", grp_id"+props.getProperty("group.id"));
                       // System.out.println("Batch cnt: "+records.count()+"---rec value:"+record.value());
                        if(( rCnt % this.p_split_cnt)==0) {
                            System.out.println(rCnt%this.p_split_cnt);
                            this.closeGzipFIle();
                            fileSeq = fileSeq + 1;
                            this.crtGzipFile("./test"+String.valueOf(fileSeq)+".gz");
                        }
                    }
                    consumer.commitSync();
                    eTime = System.currentTimeMillis();
                    if ((eTime - sTime) >= (p_RuntimeSec * 1000 )){
                        System.out.println("Time up for userparam.runtime.sec : "+p_RuntimeSec);
                        break;
                    }
                }
            }catch (Exception e){
                System.out.println("####---->excep");
                this.closeGzipFIle();
                e.printStackTrace();
            }
            finally{
                System.out.println("####---->finally");
                this.closeGzipFIle();
                consumer.close();
            }
        }
    
        public static void main(String[] args) throws Exception{
            //args[0] ---- public properties;
            //args[1] ---- local properties;
            //args[2] ---- target file prefix
            Consumer cs = new Consumer(args);
            //Hook stop signal close write buffer
            System.out.println(">>>hook TERM");
            Signal.handle(new Signal("TERM"),cs);
            Signal.handle(new Signal("INT"),cs);
            System.out.println(">>>start consumer doWork");
    
            cs.doWork();
            System.out.println("Finish all job \n");
        }
    }
