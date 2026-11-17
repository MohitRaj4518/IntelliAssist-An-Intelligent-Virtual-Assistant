"""
functions/knowledge_engine.py
Comprehensive Local Knowledge Engine and Direct Question Answering System.
Provides instant, factual, high-quality answers to queries across Science,
Computer Science, Programming, Mathematics, AI, History, Geography, and Conversational Personal Assistant inquiries without requiring external paid APIs.
"""

import re
import math
import operator

# Mathematical expressions evaluator
SAFE_OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '//': operator.floordiv,
    '%': operator.mod,
    '^': operator.pow,
    '**': operator.pow,
}


def evaluate_math_expression(query):
    """
    Detects and safely computes arithmetic expressions in natural language.
    e.g. "what is 25 * 4", "calculate 100 / 4", "15 + 32", "square root of 144", "2^8".
    """
    q = query.lower().strip()

    # Square root
    sqrt_match = re.search(r'(?:square root of|sqrt|root of)\s+([0-9]+(?:\.[0-9]+)?)', q)
    if sqrt_match:
        val = float(sqrt_match.group(1))
        res = math.sqrt(val)
        res_str = int(res) if res.is_integer() else round(res, 4)
        return f"The square root of {val} is {res_str}."

    # Factorial
    fact_match = re.search(r'(?:factorial of|fact)\s+([0-9]+)', q)
    if fact_match:
        val = int(fact_match.group(1))
        if val <= 20:
            res = math.factorial(val)
            return f"The factorial of {val} ({val}!) is {res}."

    # Standard 2-operand arithmetic: e.g. "what is 25 * 4", "calculate 144 / 12", "50 + 25"
    arith_match = re.search(r'([0-9]+(?:\.[0-9]+)?)\s*([\+\-\*\/\^%]|(?:\*\*))\s*([0-9]+(?:\.[0-9]+)?)', q)
    if arith_match:
        num1 = float(arith_match.group(1))
        op = arith_match.group(2)
        num2 = float(arith_match.group(3))
        try:
            if op == '+':
                res = num1 + num2
            elif op == '-':
                res = num1 - num2
            elif op in ['*', 'x', 'times']:
                res = num1 * num2
            elif op == '/':
                if num2 == 0:
                    return "Division by zero is undefined in mathematics."
                res = num1 / num2
            elif op in ['^', '**']:
                if num2 > 1000:
                    return "Exponent is too large to compute safely."
                res = num1 ** num2
            elif op == '%':
                res = num1 % num2
            else:
                return None

            n1_str = int(num1) if num1.is_integer() else num1
            n2_str = int(num2) if num2.is_integer() else num2
            res_str = int(res) if res.is_integer() else round(res, 4)
            return f"{n1_str} {op} {n2_str} = {res_str}."
        except Exception:
            return None

    return None


FACTUAL_KNOWLEDGE_BASE = {
    # Personalities
    "albert einstein": (
        "Albert Einstein (1879–1955) was a German-born theoretical physicist widely acknowledged to be one of the greatest "
        "and most influential physicists of all time. He is best known for developing the theory of relativity (special and general), "
        "which revolutionized our understanding of space, time, gravity, and the universe. He also formulated the mass–energy equivalence "
        "formula E = mc² and won the 1921 Nobel Prize in Physics for his discovery of the law of the photoelectric effect."
    ),
    "alan turing": (
        "Alan Turing (1912–1954) was an English mathematician, computer scientist, logician, and cryptanalyst widely considered "
        "the father of modern computer science and artificial intelligence. He formalized the concepts of algorithm and computation with "
        "the Turing machine, played a pivotal role in cracking intercepted Nazi Enigma codes at Bletchley Park during WWII, and proposed "
        "the Turing Test to assess machine intelligence."
    ),
    "isaac newton": (
        "Sir Isaac Newton (1643–1727) was an English polymath active as a mathematician, physicist, astronomer, and author. He formulated "
        "the laws of motion and universal gravitation, which dominated scientists' view of the physical universe for three centuries, "
        "and independently co-invented infinitesimal calculus alongside Gottfried Wilhelm Leibniz."
    ),
    "ada lovelace": (
        "Ada Lovelace (1815–1852) was an English mathematician and writer, chiefly known for her work on Charles Babbage's mechanical "
        "general-purpose computer, the Analytical Engine. She is recognized as the world's first computer programmer after publishing the "
        "first algorithm intended to be executed by a machine."
    ),
    "charles babbage": (
        "Charles Babbage (1791–1871) was an English polymath, mechanical engineer, and inventor who originated the concept of a digital "
        "programmable computer. He conceptualized the Difference Engine and the Analytical Engine, earning him the title 'father of the computer'."
    ),
    "marie curie": (
        "Marie Curie (1867–1934) was a Polish and naturalized-French physicist and chemist who conducted pioneering research on radioactivity. "
        "She was the first woman to win a Nobel Prize, the first person to win two Nobel Prizes in different scientific fields (Physics and Chemistry), "
        "and discovered the elements radium and polonium."
    ),
    "nikola tesla": (
        "Nikola Tesla (1856–1943) was a Serbian-American inventor, electrical engineer, and futurist best known for his contributions to the "
        "design of the modern alternating current (AC) electricity supply system, induction motors, and wireless radio transmission."
    ),
    "steve jobs": (
        "Steve Jobs (1955–2011) was an American visionary entrepreneur, industrial designer, and co-founder of Apple Inc. He revolutionized multiple "
        "industries including personal computing (Macintosh), animated film (Pixar), digital music (iPod/iTunes), smartphones (iPhone), and tablets (iPad)."
    ),
    "bill gates": (
        "Bill Gates (born 1955) is an American business magnate, software developer, and philanthropist who co-founded Microsoft Corporation with Paul Allen "
        "in 1975, leading the personal computer software revolution with MS-DOS and Windows."
    ),
    "elon musk": (
        "Elon Musk (born 1971) is a technology entrepreneur and business magnate who is the founder and CEO of SpaceX, CEO and product architect of Tesla, "
        "owner and CTO of X (formerly Twitter), and founder of Neuralink, xAI, and The Boring Company."
    ),
    "guido van rossum": (
        "Guido van Rossum (born 1956) is a Dutch programmer who created the Python programming language in 1989 and served as its 'Benevolent Dictator For Life' (BDFL) until 2018."
    ),
    "linus torvalds": (
        "Linus Torvalds (born 1969) is a Finnish-American software engineer who created the Linux kernel in 1991 and also designed the Git distributed version control system in 2005."
    ),
    "dennis ritchie": (
        "Dennis Ritchie (1941–2011) was an American computer scientist who created the C programming language and co-developed the Unix operating system at Bell Labs with Ken Thompson."
    ),
    "tim berners-lee": (
        "Sir Tim Berners-Lee (born 1955) is an English computer scientist best known as the inventor of the World Wide Web in 1989, who also created HTML, HTTP, and the first web browser."
    ),
    "geoffrey hinton": (
        "Geoffrey Hinton (born 1947) is a British-Canadian cognitive psychologist and computer scientist widely regarded as a 'Godfather of AI' and 'Godfather of Deep Learning'. He won the 2018 ACM Turing Award and the 2024 Nobel Prize in Physics for his foundational contributions to artificial neural networks."
    ),
    "demis hassabis": (
        "Sir Demis Hassabis (born 1976) is a British computer scientist, neuroscientist, and entrepreneur. He is the co-founder and CEO of Google DeepMind, and won the 2024 Nobel Prize in Chemistry for predicting protein structures using AlphaFold."
    ),
    "andrew ng": (
        "Andrew Ng (born 1976) is a renowned AI researcher, educator, and entrepreneur. He co-founded Coursera and DeepLearning.AI, led Google Brain, and served as Chief Scientist at Baidu."
    ),
    "narendra modi": (
        "Narendra Modi (born 1950) is an Indian politician who has been serving as the 14th Prime Minister of India since May 2014, representing the Bharatiya Janata Party (BJP)."
    ),

    # Programming Languages & Tools
    "python": (
        "Python is a high-level, interpreted, general-purpose programming language known for its clean, readable syntax and versatile support for "
        "object-oriented, functional, and procedural programming. It is the world's most popular language for Artificial Intelligence, Machine Learning, "
        "Data Science, Automation, Web Development (Flask/Django), and Scientific Computing."
    ),
    "javascript": (
        "JavaScript (JS) is a high-level, dynamic, multi-paradigm programming language that is one of the core technologies of the World Wide Web alongside HTML and CSS. "
        "Over 98% of websites use JavaScript client-side for dynamic web page behavior, and Node.js enables fast server-side execution."
    ),
    "c++": (
        "C++ is a high-performance, statically typed, compiled programming language designed by Bjarne Stroustrup as an extension of the C language. "
        "It provides low-level memory manipulation with object-oriented and generic programming capabilities, widely used in game engines, operating systems, embedded systems, and competitive programming."
    ),
    "java": (
        "Java is a widely used object-oriented programming language designed by Sun Microsystems (now Oracle) around the philosophy 'Write Once, Run Anywhere' (WORA). "
        "It compiles to bytecode that executes on any Java Virtual Machine (JVM), powering enterprise backends, Android mobile apps, and large distributed systems."
    ),
    "c": (
        "C is a foundational procedural programming language developed in 1972 by Dennis Ritchie at Bell Labs. It provides low-level memory access, a compact set of keywords, and high efficiency, forming the bedrock of modern operating systems, hardware drivers, and compilers."
    ),
    "html": (
        "HTML (HyperText Markup Language) is the standard markup language used to structure documents and elements displayed in a web browser, forming the backbone of all web pages."
    ),
    "css": (
        "CSS (Cascading Style Sheets) is a stylesheet language used to describe the presentation, layout, visual aesthetics, colors, and responsive design of documents written in HTML."
    ),
    "react": (
        "React is an open-source front-end JavaScript library developed by Meta for building user interfaces and single-page applications based on reusable declarative components and a Virtual DOM."
    ),
    "flask": (
        "Flask is a lightweight, flexible micro web framework for Python based on Werkzeug and Jinja2. It provides simplicity, rapid prototyping, and minimal boilerplate, making it ideal for web services, APIs, and AI dashboard applications."
    ),
    "django": (
        "Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design with a 'batteries-included' philosophy, including an ORM, admin panel, and robust security by default."
    ),
    "git": (
        "Git is a free and open-source distributed version control system designed by Linus Torvalds in 2005 to track changes in source code during software development, enabling branching, merging, and distributed collaboration."
    ),
    "github": (
        "GitHub is a cloud-based platform for software development and version control using Git, providing bug tracking, task management, continuous integration (CI/CD), and social networking for developers."
    ),
    "docker": (
        "Docker is an open-source platform that enables developers to automate the deployment, scaling, and management of applications inside lightweight, isolated, self-contained packages called containers."
    ),
    "kubernetes": (
        "Kubernetes (K8s) is an open-source container orchestration engine originally designed by Google for automating the deployment, scaling, management, and load balancing of containerized applications."
    ),
    "linux": (
        "Linux is a family of open-source Unix-like operating systems based on the Linux kernel, created by Linus Torvalds in 1991. It powers supercomputers, cloud infrastructure, Android devices, and web servers worldwide."
    ),
    "sql": (
        "SQL (Structured Query Language) is the standardized domain-specific programming language used to manage, query, and manipulate data stored in relational database management systems (RDBMS) like MySQL, PostgreSQL, and SQLite."
    ),
    "nosql": (
        "NoSQL (Not Only SQL) databases provide mechanisms for storage and retrieval of unstructured or semi-structured data using non-tabular schemas, such as document stores (MongoDB), key-value stores (Redis), and graph databases (Neo4j)."
    ),
    "api": (
        "An API (Application Programming Interface) is a defined set of rules, protocols, and tools that allows different software applications to communicate and exchange data with each other seamlessly."
    ),
    "rest api": (
        "A REST API (Representational State Transfer API) is an architectural style for network-based hypermedia systems that uses standard HTTP methods (GET, POST, PUT, DELETE) to manage resources represented in formats like JSON."
    ),

    # Artificial Intelligence & Machine Learning
    "artificial intelligence": (
        "Artificial Intelligence (AI) is the branch of computer science dedicated to creating software and systems capable of performing tasks "
        "that typically require human intelligence, such as learning, visual perception, reasoning, decision-making, and natural language understanding."
    ),
    "ai": (
        "Artificial Intelligence (AI) is the simulation of human intelligence in machines, enabling computers to learn from experience, adapt to new inputs, solve problems, and make autonomous decisions."
    ),
    "machine learning": (
        "Machine Learning (ML) is a subset of artificial intelligence focused on building algorithms that learn patterns and relationships directly from data, improving their accuracy and predictive performance over time without explicit rules programming."
    ),
    "deep learning": (
        "Deep Learning is a specialized subfield of machine learning based on artificial neural networks with multiple representation layers ('deep' networks). It powers state-of-the-art breakthroughs in image recognition, natural language processing, and speech recognition."
    ),
    "neural network": (
        "An Artificial Neural Network (ANN) is a computational model inspired by the biological neural networks of human brains, composed of interconnected layers of artificial nodes (neurons) that process inputs via weights, biases, and non-linear activation functions."
    ),
    "supervised learning": (
        "Supervised Learning is a category of machine learning where algorithms are trained on labeled datasets containing both input features and corresponding ground-truth target outputs (e.g., classification and regression)."
    ),
    "unsupervised learning": (
        "Unsupervised Learning is a category of machine learning where algorithms discover underlying patterns, groupings, and structures in unlabeled data without predefined target labels (e.g., clustering with K-Means, dimensionality reduction with PCA)."
    ),
    "reinforcement learning": (
        "Reinforcement Learning (RL) is a paradigm of machine learning where an autonomous agent learns optimal decision-making policies through trial-and-error interactions with an environment, maximizing cumulative rewards."
    ),
    "natural language processing": (
        "Natural Language Processing (NLP) is an interdisciplinary subfield of artificial intelligence, computer science, and linguistics concerned with enabling computers to understand, interpret, process, and generate human languages."
    ),
    "computer vision": (
        "Computer Vision is a field of artificial intelligence that trains computers to interpret and understand visual information from the world, extracting meaningful attributes from digital images and videos."
    ),
    "large language model": (
        "A Large Language Model (LLM) is an advanced deep learning model based on the transformer architecture, trained on vast corpora of text data using self-supervised learning to comprehend and generate human-like natural language."
    ),
    "llm": (
        "A Large Language Model (LLM) is a deep neural network (such as GPT-4 or Gemini) trained on hundreds of billions of words to understand context, generate coherent text, write code, and answer complex queries."
    ),
    "chatgpt": (
        "ChatGPT is an AI chatbot developed by OpenAI, launched in November 2022, powered by the GPT series of generative pretrained transformer models."
    ),
    "transformer": (
        "The Transformer is a deep learning model architecture introduced in 2017 in the landmark paper 'Attention Is All You Need'. It replaces recurrent mechanisms with self-attention, allowing parallel processing of sequential data and underpinning modern LLMs."
    ),
    "overfitting": (
        "Overfitting occurs in machine learning when a model learns the training data, noise, and outliers too closely, resulting in high training accuracy but poor generalization to unseen validation and test data."
    ),
    "underfitting": (
        "Underfitting occurs when a machine learning model is too simple to capture the underlying structure or relationships in the data, leading to poor predictive performance on both training and test datasets."
    ),
    "gradient descent": (
        "Gradient Descent is a first-order iterative optimization algorithm used to minimize an objective loss function by iteratively updating model parameters in the direction of the negative gradient."
    ),
    "backpropagation": (
        "Backpropagation (backward propagation of errors) is the fundamental algorithm used to train neural networks. It computes the gradient of the loss function with respect to each network weight using the chain rule of calculus, flowing backwards from output to input."
    ),
    "turing test": (
        "The Turing Test, proposed by Alan Turing in 1950, is a test of a machine's ability to exhibit intelligent behavior indistinguishable from that of a human through natural language conversation."
    ),

    # Computer Science & Data Structures
    "algorithm": (
        "An algorithm is a finite, unambiguous, step-by-step sequence of instructions or rules designed to perform a specific computational task or solve a particular class of problems."
    ),
    "data structure": (
        "A data structure is a specialized format for organizing, storing, and managing data efficiently in computer memory, such as arrays, linked lists, stacks, queues, trees, and graphs."
    ),
    "big o notation": (
        "Big O notation is a mathematical notation used in computer science to describe the limiting behavior and asymptotic upper bound of an algorithm's time or space complexity as input size n approaches infinity."
    ),
    "binary search": (
        "Binary Search is an efficient divide-and-conquer search algorithm that finds the position of a target value within a sorted array in O(log n) time by repeatedly halving the search interval."
    ),
    "recursion": (
        "Recursion is a programming technique and mathematical method where a function solves a problem by calling itself with smaller sub-instances until reaching a terminating base condition."
    ),
    "dynamic programming": (
        "Dynamic Programming (DP) is an algorithmic paradigm that solves complex problems by breaking them into overlapping subproblems, solving each subproblem only once, and storing the results in memory (memoization or tabulation)."
    ),
    "operating system": (
        "An Operating System (OS) is system software that manages computer hardware, system resources (CPU, RAM, storage, I/O devices), and provides common services and execution environments for application programs."
    ),
    "deadlock": (
        "A deadlock in operating systems is a situation where a set of processes are permanently blocked because each process holds a resource and waits for another resource held by another process in the set."
    ),
    "cloud computing": (
        "Cloud Computing is the on-demand delivery of computing services—including servers, storage, databases, networking, software, and analytics—over the internet ('the cloud') with pay-as-you-go pricing."
    ),
    "cybersecurity": (
        "Cybersecurity is the practice of protecting computer systems, networks, devices, and digital data from malicious digital attacks, unauthorized access, theft, or disruption."
    ),
    "blockchain": (
        "A blockchain is a decentralized, distributed, and immutable digital ledger that securely records transactions across a peer-to-peer network using cryptographic hashes and consensus protocols."
    ),
    "cryptography": (
        "Cryptography is the practice and study of techniques for secure communication in the presence of adversaries, encompassing encryption, decryption, digital signatures, and cryptographic hash functions."
    ),

    # Science & Mathematics
    "gravity": (
        "Gravity is a fundamental natural interaction in physics whereby all things with mass or energy—including planets, stars, galaxies, and light—are attracted toward one another. In General Relativity, it is described as the curvature of spacetime caused by mass and energy."
    ),
    "quantum mechanics": (
        "Quantum Mechanics is the fundamental branch of physics that describes the behavior of matter and light at atomic and subatomic scales, characterized by wave-particle duality, quantization of energy, the uncertainty principle, and quantum entanglement."
    ),
    "speed of light": (
        "The speed of light in a vacuum is exactly 299,792,458 meters per second (approximately 300,000 km/s or 186,282 miles per second), denoted by 'c', which represents the universal speed limit in physics."
    ),
    "speed of sound": (
        "The speed of sound in dry air at 20°C (68°F) is approximately 343 meters per second (1,235 km/h or 767 mph)."
    ),
    "photosynthesis": (
        "Photosynthesis is the biological process used by plants, algae, and certain bacteria to convert light energy (sunlight) into chemical energy (glucose), releasing oxygen as a byproduct from carbon dioxide and water: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂."
    ),
    "dna": (
        "DNA (Deoxyribonucleic Acid) is the molecule that carries the genetic instructions used in the growth, development, functioning, and reproduction of all known living organisms and many viruses, arranged in a double helix structure."
    ),
    "black hole": (
        "A black hole is a region of spacetime where gravity is so strong that nothing—no particles or even electromagnetic radiation such as light—can escape from inside its event horizon."
    ),
    "solar system": (
        "The Solar System is the gravitationally bound system of the Sun and the objects that orbit it, including eight planets (Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune), dwarf planets (such as Pluto), moons, asteroids, and comets."
    ),
    "milky way": (
        "The Milky Way is the barred spiral galaxy containing our Solar System, spanning approximately 100,000 light-years in diameter and containing an estimated 100 to 400 billion stars."
    ),
    "calculus": (
        "Calculus is the mathematical study of continuous change, divided into differential calculus (concerning instantaneous rates of change and slopes of curves) and integral calculus (concerning accumulation of quantities and areas under curves)."
    ),
    "pi": (
        "Pi (π) is the mathematical constant representing the ratio of a circle's circumference to its diameter, approximately equal to 3.1415926535... It is an irrational number with infinite non-repeating decimal digits."
    ),
    "fibonacci sequence": (
        "The Fibonacci sequence is an integer sequence where each number is the sum of the two preceding ones, typically starting with 0 and 1: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89... The ratio of consecutive terms converges to the Golden Ratio (φ ≈ 1.618)."
    ),

    # Geography & General Facts
    "capital of france": "The capital and largest city of France is Paris.",
    "capital of india": "The capital of India is New Delhi.",
    "capital of usa": "The capital of the United States of America is Washington, D.C.",
    "capital of united states": "The capital of the United States is Washington, D.C.",
    "capital of uk": "The capital of the United Kingdom is London.",
    "capital of united kingdom": "The capital of the United Kingdom is London.",
    "capital of japan": "The capital of Japan is Tokyo.",
    "capital of germany": "The capital of Germany is Berlin.",
    "capital of canada": "The capital of Canada is Ottawa.",
    "capital of australia": "The capital of Australia is Canberra.",
    "capital of china": "The capital of China is Beijing.",
    "capital of russia": "The capital of Russia is Moscow.",
    "capital of italy": "The capital of Italy is Rome.",
    "capital of spain": "The capital of Spain is Madrid.",
    "capital of brazil": "The capital of Brazil is Brasília.",
    "largest ocean": "The largest and deepest ocean on Earth is the Pacific Ocean, covering more than 60 million square miles.",
    "tallest mountain": "The tallest mountain on Earth above sea level is Mount Everest, standing at 8,848.86 meters (29,031.7 feet) in the Himalayas.",
    "longest river": "The longest river in the world is traditionally recognized as the Nile River in Africa (approximately 6,650 km), closely followed by the Amazon River."
}


def lookup_local_knowledge(query):
    """
    Looks up factual questions in the built-in comprehensive knowledge base.
    Matches queries by exact topic, prefix patterns, and semantic keywords.
    """
    q = query.lower().strip()

    # 1. Check math expressions first
    math_ans = evaluate_math_expression(q)
    if math_ans:
        return math_ans

    # 2. Direct exact match
    if q in FACTUAL_KNOWLEDGE_BASE:
        return FACTUAL_KNOWLEDGE_BASE[q]

    # 3. Strip common question prefixes
    clean_topic = q
    prefixes = [
        'who is', 'who was', 'who were',
        'what is', 'what are', 'what was', 'what were',
        'tell me about', 'explain', 'define', 'meaning of',
        'what does', 'how does', 'how do', 'where is', 'which is'
    ]
    for p in prefixes:
        if clean_topic.startswith(p + ' '):
            clean_topic = clean_topic[len(p):].strip()
            # remove leading 'the', 'a', 'an'
            for art in ['the ', 'a ', 'an ']:
                if clean_topic.startswith(art):
                    clean_topic = clean_topic[len(art):].strip()
            break

    # Strip trailing punctuation
    clean_topic = clean_topic.rstrip('?.! ')

    # Check cleaned topic
    if clean_topic in FACTUAL_KNOWLEDGE_BASE:
        return FACTUAL_KNOWLEDGE_BASE[clean_topic]

    # 4. Partial substring or keyword matching across knowledge base
    for key, answer in FACTUAL_KNOWLEDGE_BASE.items():
        if key == clean_topic:
            return answer
        # If the key is a clean multi-word phrase inside the query
        if len(key) >= 4 and key in clean_topic:
            return answer
        # If the clean topic is inside the key
        if len(clean_topic) >= 4 and clean_topic in key:
            return answer

    return None
