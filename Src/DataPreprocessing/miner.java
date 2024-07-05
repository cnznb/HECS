import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.csvreader.CsvWriter;
import gr.uom.java.xmi.UMLModel;
import gr.uom.java.xmi.UMLModelASTReader;
import gr.uom.java.xmi.decomposition.AbstractCodeFragment;
import gr.uom.java.xmi.decomposition.AbstractCodeMapping;
import gr.uom.java.xmi.decomposition.UMLOperationBodyMapper;
import gr.uom.java.xmi.decomposition.replacement.Replacement;
import gr.uom.java.xmi.diff.UMLModelDiff;
import org.eclipse.jgit.lib.Repository;
import org.refactoringminer.api.GitHistoryRefactoringMiner;
import org.refactoringminer.api.GitService;
import org.refactoringminer.api.Refactoring;
import org.refactoringminer.api.RefactoringHandler;
import org.refactoringminer.rm1.GitHistoryRefactoringMinerImpl;
import org.refactoringminer.util.GitServiceImpl;


import java.io.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Set;
import java.util.Vector;
import java.util.concurrent.TimeUnit;

public class test {
    public static void python(String cmd){
        try {
            Process proc = Runtime.getRuntime().exec(cmd);
            proc.waitFor();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
    public static void mkdir(String path){
        Path paths = Paths.get(path);
        try {
            Files.createDirectories(paths);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
//    public static boolean solve() throws Exception{
//        GitService gitService = new GitServiceImpl();
//        GitHistoryRefactoringMiner miner = new GitHistoryRefactoringMinerImpl();
//
//        Repository repo = gitService.cloneIfNotExists(
//                "E:/IdeaProjects/Practise/",
//                "");
//        miner.detectAtCommit(repo, "ab98bcacf6e5bf1c3a06f6bcca68f178f880ffc9", new RefactoringHandler() {
//            @Override
//            public void handle(String commitId, List<Refactoring> refactorings) {
//                for (Refactoring ref : refactorings) {
//                    System.out.println(ref.getName());
//                    if(ref.getName().equals("Extract Class")){
//                        //路径为你要保存的数据集路径
//                        String path = "E:\\dataset\\java-algorithms-implementation\\"+id;
//                        try {
//                            mkdir(path);
//                            //eg:  D:\dataset\antlr4\10000\log.json
//                            File f = new File(path+"\\"+"log.json");
//
//                            Writer writer = new OutputStreamWriter(new FileOutputStream(f),StandardCharsets.UTF_8);
//                            writer.write(commitId+'\n');
//                            writer.flush();
//                            writer.write(ref.toJSON());
//                            writer.flush();
//                            writer.close();
//                        } catch (IOException e) {
//                            e.printStackTrace();
//                        }
//                        //把JSON字符串转为对象
//                        ref_json rj = JSON.parseObject(ref.toJSON(), ref_json.class);
//                        //调用python脚本，假设脚本地址为D:\git_utils.py  获得old文件保存至eg：D:\dataset\antlr4\10000\old.java
//                        String cmd="python D:\\Pworkspace\\R&M\\get_dataset\\git_utils.py 2 " +
//                                rj.getLeftSideLocations().get(0).getFilePath() +
//                                " " + path + "\\old.java" +
//                                " E:/IdeaProjects/Practise/" +
//                                " "+ commitId;
//                        python(cmd);
//                        id++;
//                    }
//                }
//            }
//        });
//        return true;
//    }
    public static int id = 10000;
    //copy from source_path to target_path
    public static void copy_java(String source_path, String target_path) throws Exception {
        File sourceFile = new File(source_path);
        File destinationDir = new File(target_path);

        if (!sourceFile.exists()) {
            return;
        }

        File destinationFile = new File(destinationDir, sourceFile.getName());

        InputStream inputStream = new FileInputStream(sourceFile);
        OutputStream outputStream = new FileOutputStream(destinationFile);

        byte[] buffer = new byte[1024];
        int length;

        while ((length = inputStream.read(buffer)) > 0) {
            outputStream.write(buffer, 0, length);
        }

        inputStream.close();
        outputStream.close();
    }
    // demo of usage for refactoringminer
    public static void main(String args[]) throws Exception {
        GitService gitService = new GitServiceImpl();
        GitHistoryRefactoringMiner miner = new GitHistoryRefactoringMinerImpl();
        // the cloned project path
        // neo4j drools
        String project_path = "E:\\IdeaProjects\\Miner\\tmp\\intellij-community\\"; //1
        Repository repo = gitService.cloneIfNotExists(project_path, "");
        // The commit ID you want to test is sha1 in the JSON file
        /**
         * fcc9a34356817d93c24b5ccf3107ec234a28b136
         * 08b1b56e2cd5ad72126f4bbeb15a47d9b104dfff
         */
        String commitID = "f8777ef36ab66e2c75e9fc2223473d68f5b1263b";  //2
        miner.detectAtCommit(repo, commitID, new RefactoringHandler() {
            @Override
            public void handle(String commitId, List<Refactoring> refactorings) {
                for (Refactoring ref : refactorings) {
                    // The type of refactoring you want to test
                    String refactoring_type = "Extract Class";  //3   ES
                    // Which file directory do you want to save the information to
                    String[] parts = project_path.split("\\\\");
                    String refactoring_file_name = parts[parts.length-1];   //4
                    //System.out.println(ref.getName());
                    if(ref.getName().equals(refactoring_type)){
                        System.out.println("++");
                        System.out.println(ref.getName());
                        // The path to the dataset you want to save
                        ref_json rrj = JSON.parseObject(ref.toJSON(), ref_json.class);
                        String filePath = rrj.getLeftSideLocations().get(0).getFilePath();
                        String fileName = filePath.split("/")[filePath.split("/").length-1].split("\\.")[0];
                        // Which directory do you want to place the files in
                        String path = "E:\\HMove\\dataset\\train\\" + refactoring_file_name + "\\" + fileName + "\\"; //5
                        try {
                            while(new File(path + id).exists())id++;
                            path += id;
                            mkdir(path);
                            //eg:  D:\dataset\antlr4\10000\log.json
                            File f = new File(path+"\\"+"log.json");

                            Writer writer = new OutputStreamWriter(new FileOutputStream(f),StandardCharsets.UTF_8);
                            writer.write(commitID +'\n');
                            writer.flush();
                            writer.write(ref.toJSON());
                            writer.flush();
                            writer.close();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                        // Convert JSON strings to objects
                        // Calling Python script, assuming the script address is on the desktop, retrieve the code before refactoring
                        String cmd="python src/main/resources/git_utils.py 2 " +
                                rrj.getLeftSideLocations().get(0).getFilePath() +
                                " " + path + "\\source.java" +
                                " " + project_path +
                                " " + commitID;
                        python(cmd);
                        // Calling Python script, assuming the script address is on the desktop, retrieve the refactored code
                        cmd="python src/main/resources/git_utils.py 4 " +
                                rrj.getRightSideLocations().get(0).getFilePath() +
                                " " + path + "\\target.java" +
                                " " + project_path +
                                " " + commitID;
                        python(cmd);
                        id++;
                    }
                }
            }
        });
    }
    public static void printResults(Process process) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String line = "";
        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }
    }
}
/**
 * c9b2006381301c99b66c50c4b31f329caac06137
 * ebb1c2c364e888d4a0f47abe691cb2bad4eb4e75
 * e58c9c3eef4c6e44b21a97cfbd2862bb2eb4627a
 * d47e58f9bbce9a816378e8a7930c1de67a864c29
 */