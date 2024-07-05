import os
import openai

message_list = [
    {
        "You are an expert Java programer. Your task is to extract and identify entities and methods in Java code based on the sample knowledge and rules I provide you."},
    {'''
    Knowledge 1: 
        You need to learn to extract the correct abstract methods. Here are three examples which divided into code snippet, example input, and example output:
        Example1:
        1. Code Snippet:
        abstract class A {
            public abstract void m2();
        }
        2. Example Input: Does the code snippet has the abstract methods? If yes, please print the Example Output as follow: yes, Class name.method1,method2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: yes, A.m2.
        Example2:
        1. Code Snippet:
        interface MyInterface {
            void abstractMethod();
        }
        class B implements MyInterface {
            public void abstractMethod() {
            }
        }
        2. Example Input: Does the code snippet has the abstract methods? If yes, please print the Example Output as follow: yes, Class name.method1,method2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: yes, B.abstractMethod().
        Example3:
        1. Code Snippet:
        class A {
            System.out.println("Testing.");
        }
        2. Example Input: Does the code snippet has the abstract methods? If yes, please print the Example Output as follow: yes, Class name.method1,method2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: no.
        Please refer to the examples above to learn the process of correctly extracting abstract methods from a class and display the results in the format of Class name.method1,method2.... This knowledge will be used in the subsequent sample validation.
     '''
     },
    {'''
    This is a code snippet: 
    abstract class B {
      public abstract void m0();
      public abstract void m1();
    }
    Does the code snippet has Knowledge 1 relevant field? If yes, please extract the abstract methods according to the Knowledge 1 and present them.
    '''
     },
    {'''
    Knowledge 2: 
        You need to learn to extract methods that override an abstract or concrete method of superclass. Here is four examples which divided into code snippet, example input, and example output:
        Example 1:
        1. Code Snippet:
        abstract class A {
            public abstract void m1();
            }
        }
        class B extends A{
            @Override
            public void m1(){
                System.out.println("Yes");
            }
        }
        2. Example Input: Does the code snippet has the methods that override an abstract or concrete method of superclass? If yes, please print the Example Output as follow: yes, Class name.method1,method2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: yes, B.m1.
        Example 2:
        1. Code Snippet:
        abstract class A{
            public void m1() { 
            System.out.println("Testing.");
        }
        }
        class B extends A{
            @Override
            public void m1(){
                System.out.println("Yes");
            }
        }
        2. Example Input: Does the code snippet has the methods that override an abstract or concrete method of superclass? If yes, please print the Example Output as follow: yes, Class name.method1,method2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: yes, B: m1.
        Example 3:
        1. Code Snippet:
        abstract class A {
            public abstract void m1();
            public void m2() { 
                    System.out.println("Testing.");
            }
        }
        class B extends A{
            @Override
            public void m1(){
                System.out.println("Yes");
            }
            @Override
            public void m2(){
                System.out.println("No");
            }
        }
        2. Example Input: Does the code snippet has the methods that override an abstract or concrete method of superclass? If yes, please print the Example Output as follow: yes, Class name.method1,method2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: yes, B: m1,m2.
        Example 4:
        1. Code Snippet:
        class A {
            System.out.println("Testing.");
        }
        2. Example Input: Does the code snippet has the methods that override an abstract or concrete method of superclass? If yes, please print the Example Output as follow: yes, Class name.method1,method2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: no.
        Please refer to the examples above to learn the process of correctly extracting the methods that override an abstract or concrete method of superclass and display the results in the format of class name.method1,method2.... This knowledge will be used in the subsequent sample validation.
    '''
     },
    {'''
    This is a code snippet: 
    abstract class A {
        public abstract void m1();
        public int m2(){
            System.out.println("Testing2.");
        } 
        public int m3(){
            System.out.println("Testing3.");
        }
    }
    class B extends A{
        @Override
        public void m1(){
            System.out.println("Yes");
        }
        @Override
        public void m2(){
            System.out.println("No");
        }
    }
    Does the code snippet has Knowledge 2 relevant field? If yes, please extract the methods that override an abstract or concrete method of superclass according to the Knowledge 2 and present them.
    '''
     },
    {'''
    Knowledge 3:
        You need to learn to extract the fields accessed by other classes. Here are four examples which divided into code snippet, example input, and example output:
        Example1:
        1. Code Snippet:
        class A {
            private int f0 = 1;
            private int f1;
            private int f2;
            public void m1(int x,int y){
                    f1 = x;
                    f2 = y;
            }
        }
        class B {
            A a = new A();
            void m1{
                a.m1(1,2);
            }
        }
        2. Example Input: Does the code snippet has the fields accessed by other classes? If yes, please print the Example Output as follow: yes, Class name.field1,field2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: yes, A.f1,f2.
        Example2:
        1. Code Snippet:
        class A {
            private int f0 = 1;
        }
        class B {
            A a = new A();
            int b = a.f0;
        }
        2. Example Input: Does the code snippet has the fields accessed by other classes? If yes, please print the Example Output as follow: yes, Class name.field1,field2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: yes, A.f0.
        Example3:
        1. Code Snippet:
        class A {
            static int f0 = 10;
        }
        class B {
            System.out.println(A.f0)
        }
        2. Example Input: Does the code snippet has the fields accessed by other classes? If yes, please print the Example Output as follow: yes, Class name.field1,field2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: yes, A.f0.
        Please refer to the examples above to learn the process of correctly extracting the fields accessed by other classes and display the results in the format of Class name. field1,field2.... This knowledge will be used in the subsequent sample validation.
    '''
     },
    {'''
    This is a code snippet: 
    class B {
        private int f1;
        public void m1(int val){
                f1 = val;
        }
    }
    class C {
        B b = new B()
        void m1(){
            b.m1(10);
        }
    }
    Does the code snippet has Knowledge 3 relevant field? If yes, please extract the methods that override an abstract or concrete method of superclass according to the Knowledge 3 and present them.
    '''
     },
    {'''
    Knowledge 4:
        You need to learn to extract the methods that have any super method invocations. Here are two examples which divided into code snippet, example input, and example output:
        Example1:
        1. Code Snippet:
        class A {
        public void m1(){
                System.out.println("Parent method");
        }
        }
        class B extends A{
        public void m2() {
                m1(); 
                System.out.println("Child method");
        }
        }
        2. Example Input: Does the code snippet has the methods that have any super method invocations? If yes, please print the Example Output as follow: yes, Class name.method1,method2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: yes, A.m1.
        Example2:
        1. Code Snippet:
        class A {
            System.out.println("Testing.");
        }
        2. Example Input: Does the code snippet has the methods that have any super method invocations? If yes, please print the Example Output as follow: yes, Class name.method1,method2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: no.
        Please refer to the examples above to learn the process of correctly extracting the methods that have any super method invocations and display the results in the format of Class name.method1,method2.... This knowledge will be used in the subsequent sample validation.
    '''
     },
    {
        '''
    This is a code snippet: 
    class A {
        public void m1(){
        System.out.println("Parent method");
        }
    }
    class B extends A{
        public void m2() {
        m1();
        System.out.println("Child method");
        }
        public void m3() {
        System.out.println("Child method");
        }
    }
    Does the code snippet has Knowledge 4 relevant field? If yes, please extract the methods that have any super method invocations according to the Knowledge 4 and present them.
    '''
    },
    {
        '''
    Knowledge 5:
        You need to learn to extract the methods that are synchronized or have a synchronized block should not be extracted. Here are three examples which divided into code snippet, example input, and example output:
        Example1:
        1. Code Snippet:
        class A {
            private int count = 0;
            public synchronized void m1() {
                count++;
                System.out.println("Count: " + count);
            }
        }
        2. Example Input: Does the code snippet has the methods that are synchronized or have a synchronized block? If yes, please print the Example Output as follow: yes, Class name.method1,method2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: yes, A.m1.
        Example2:
        1. Code Snippet:
        class A {
            public void m1() {
                synchronized (this) {
                    System.out.println("Performing task...");
                }
            }
        }
        2. Example Input: Does the code snippet has the methods that are synchronized or have a synchronized block? If yes, please print the Example Output as follow: yes, Class name.method1,method2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: yes, A.m1.
        Example3:
        1. Code Snippet:
        class A {
            System.out.println("Testing.");
        }
        2. Example Input: Does the code snippet has the methods that are synchronized or have a synchronized block? If yes, please print the Example Output as follow: yes, Class name.method1,method2.... Otherwise, please print the Example Output as follow: no.
        3. Example Output: no.
        Please refer to the examples above to learn the process of correctly extracting the methods that are synchronized or have a synchronized block and display the results in the format of Class name.method1,method2.... This knowledge will be used in the subsequent sample validation.
    '''
    },
    {
        '''
    This is a code snippet:
    class A {
        int m1(){ synchronized (this){...} }
    }
    Does the code snippet has Knowledge 5 relevant field? If yes, please extract the methods that are synchronized or have a synchronized block according to the Knowledge 5 and present them.
    '''
    },
    {'''
    Knowledge 6:
        You need to learn how to determine if the extracted class  contain more than one field or method. Here is three examples which divided into Source Class, Extracted Class, Example Input, and Example Output. Finally, the objects in Extracted Class are fields or methods extracted from Source Class:
        Example1:
        1. Source Class:
        class A {
            private int count = 0;
            public synchronized void m0() {
                count++;
                System.out.println("Count: " + count);
            }
            public void m1() {
                synchronized (this) {
                    System.out.println("Performing task...");
                }
            }
        }
        2. Extracted Class:
        R.count,m0.
        3. Example Input: Does the Extracted Class contain more than one field or method? If yes, please print the Example Output as follow: yes. Otherwise, please print the Example Output as follow: no.
        4. Example Output: yes.
        Example2:
        1. Source Class:
        class A {
            private int count = 0;
            public synchronized void m0() {
                count++;
                System.out.println("Count: " + count);
            }
            public void m1() {
                synchronized (this) {
                    System.out.println("Performing task...");
                }
            }
        }
        2. Extracted Class:
        R.count.
        3. Example Input: Does the Extracted Class contain more than one field or method? If yes, please print the Example Output as follow: yes. Otherwise, please print the Example Output as follow: no.
        4. Example Output: no.
        Example3:
        1. Source Class:
        class A {
            private int count = 0;
            public synchronized void m0() {
                count++;
                System.out.println("Count: " + count);
            }
            public void m1() {
                synchronized (this) {
                    System.out.println("Performing task...");
                }
            }
        }
        2. Extracted Class:
        R.m0.
        3. Example Input: Does the Extracted Class contain more than one field or method? If yes, please print the Example Output as follow: yes. Otherwise, please print the Example Output as follow: no.
        4. Example Output: no.
        Please refer to the examples above to learn the process of correctly determine if the Extracted Class  contain more than one field or method. This knowledge will be used in the subsequent sample validation.
    '''
     },
    {'''
    This is a Source Class:
    class A {
        int x;
        int m2(){ synchronized (this){...} }
    }
    Its Extracted Class:
    R.x,m2
    Does the Extracted Class contain more than one field or method? If yes, please print yes. Otherwise, please print no.
    '''
     },
    {'''
    Now please explain the Knowledge1 to Knowledge6 that I have taught you.
    '''
     },
    {'''
    Now, I will give you 6 Pre-Condition rules for judging the output of extracting intra class information from the source code. Please combine the knowledge 1 to 6 previously provided to you to learn.Then, I will give you a simple of input which you should analyze. The rules as follows:
    P1. Abstract methods should not be extracted.
    P2. Methods that override an abstract or concrete method of superclass should not be extracted.
    P3. Fields accessed by other classes should not be extracted.
    P4. Methods that have any super method invocations should not be extracted.
    P5. Methods that are synchronized or have a synchronized block should not be extracted.
    P6. The extracted class should contain more than one field or method.
    '''
     },
    {'''
    Sample Input are divided into Source Code, Extracted Class, Target:
    1. Source Code:
    '''
     + Source_Code + '''
    2. Extracted Class :
    R.f2, m2.
    3. Target: 
    3.1 Please verify whether the the fileds or methods in Extracted Class can be extracted by Classes in  Source Code through Knowledge1 to Knowledge5 (Violate P1 to P5). Fileds or methods outside the extracted class description do not need to be detected.
    3.2 Does the Extracted Class contain more than one field or method?(obey the Rule6).  
    3.3 If there are violations of P1 to P5, please print Failed on the last line of the inference result.
    3.4 If P6 cannot be met, please print Failed on the last line of the inference result..
    3.5 Otherwise, please print Success on the last line of the inference result.
    '''
     }]


# Construct OpenAI requests
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,  # Control the randomness of model output
    )
    return response


# Sending OpenAI requests and obtaining replies, similar to an interactive interface, implements contextual functionality
def start_communication(message):
    conversation_history.append({'role': 'user', 'content': message})
    response = get_completion_from_messages(conversation_history)
    print(response.choices[0].message["content"])
    conversation_history.append({'role': 'assistant', 'content': response.choices[0].message["content"]})


if __name__ == "__main__":
    # Initialize OpenAI API   
    openai.api_key = os.getenv("sk-xxx")
    index = 0
    # Defining Dialogue History
    conversation_history = [
        {'role': 'system', 'content': 'You are a helpful assistant.'}
    ]
    # Read relevant source code from a file
    file_path = r'D:\Scripts\SourceCode.txt'
    with open(file_path, 'rb') as file:
        content = file.read().decode('utf-8')
        Source_Code = content
    while index < 16:
        user_input = message_list[index]
        start_communication(user_input)
        index += 1
    index = 0
