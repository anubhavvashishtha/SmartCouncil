# Multi-Agent Orchestration System

> An intelligent task decomposition and parallel execution framework powered by Small Language Models (SLMs)

## 🎯 Core Philosophy

**The Problem**: Traditional multi-agent systems either execute tasks sequentially (slow) or blindly parallelize everything (breaks dependencies). They also struggle with task decomposition - creating too many artificial subtasks or missing natural parallelization opportunities.

**Our Solution**: An orchestration layer that uses SLMs to:
1. Intelligently decompose complex prompts into subtasks
2. Identify true dependencies vs. artificial ones
3. Maximize parallel execution while respecting task order
4. Optimize the task graph to remove redundancy

---

## 🏗️ Architecture Overview
![alt text](<architecture/Architecture Overview.png>)


---

## 🎬 Example 1: Simple Sequential Workflow

**User Prompt**: 
```
"Create a sleep schedule for better gym recovery"
```

### Task Decomposition Phase
```
{
  "tasks": [{
    "id": "t1",
    "description": "Create sleep schedule for gym recovery",
    "agent": "Sleep",
    "depends_on": []
  }]
}
```



**Decision Logic**: Single, focused task - no decomposition needed.

### Execution Flow
![alt text](<architecture/Execution Flow for single prompt.png>)


**Why No Decomposition?**
- Single domain (Sleep)
- Single action (create schedule)
- No explicit sequential steps
- Context is naturally included in one task

---

## 🎬 Example 2: Complex Multi-Agent Workflow

**User Prompt**: 
```
"Compare HIIT vs steady cardio for fat loss, then create a diet plan based on the better option for someone with high blood pressure"
```

### Task Decomposition Phase
```
{
  "tasks": [{
    "id": "t1",
    "description": "Compare HIIT vs steady cardio for fat loss",
    "agent": "Exercise",
    "depends_on": []
  },
  {
    "id": "t2",
    "description": "Validate exercise safety for high blood pressure",
    "agent": "Medical",
    "depends_on": [t1]
  },
  {
    "id": "t3",
    "description": "Create diet plan based on recommended exercise",
    "agent": "Diet",
    "depends_on": [t1, t2]
  }
  ]
}
```

**Decision Logic**:
- **t1**: Independent research - can start immediately
- **t2**: Needs t1's recommendation to validate safety
- **t3**: Needs both t1 (which exercise) and t2 (safety validation)

### Optimization Phase

**Before Optimization** (hypothetical over-decomposition):
```
t1: Research HIIT benefits
t2: Research steady cardio benefits  
t3: Compare HIIT vs steady cardio
t4: Validate for blood pressure
t5: Create diet plan
```

**After Optimization** (actual):
```
t1: Compare HIIT vs steady cardio for fat loss
t2: Validate exercise safety for high blood pressure
t3: Create diet plan based on recommendation
```

**Optimization Rules Applied**:
- ❌ Removed t1, t2 (redundant) - comparison naturally includes research
- ✅ Kept t1, t2, t3 separate - different analytical dimensions
- ✅ Preserved dependencies - each task needs prior results

### Execution Flow
![alt text](<architecture/Execution Flow.png>)


### Parallel vs Sequential Decision
![alt text](<architecture/Parallel vs Sequential Decision.png>)


## 🧠 Intelligent Decision Making

### Dependency Resolver Logic

```python
def get_ready_tasks():
    completed = get_completed_task_ids()
    pending = get_pending_tasks()
    
    ready = []
    for task in pending:
        # Check if ALL dependencies are completed
        if set(task.depends_on) ⊆ set(completed):
            ready.append(task)
    
    return ready
```
![alt text](<architecture/Untitled diagram-2025-12-08-140058.png>)


---

## 📊 Database Schema
![alt text](<architecture/Database Schema.png>)


**State Transitions**:
![alt text](<architecture/State Transitions.png>)


---

## 🚀 Key Features

### 1. **Smart Decomposition**
- LLM analyzes prompt structure
- Identifies explicit vs implicit tasks
- Avoids artificial sub-tasking
- Preserves user intent

### 2. **Dependency Intelligence**
- Distinguishes true dependencies from parallel work
- Uses subset logic: `depends_on ⊆ completed`
- Maximizes concurrent execution
- Prevents circular dependencies

### 3. **Optimization Layer**
- Removes redundant research tasks
- Merges linear chains
- Preserves multi-dimensional analysis
- Maintains parallelization opportunities

### 4. **Context Propagation**
```python
task["previous_tasks"] = get_completed_task_responses(task["depends_on"])
```
Dependent tasks receive only relevant prior results, not the entire history.

### 5. **Specialized Agents**
Each agent has strict boundaries:
- **Sleep**: Schedules, circadian rhythm, recovery
- **Exercise**: Workouts, training plans, form
- **Diet**: Nutrition, macros, meal planning
- **Medical**: Safety validation, symptom interpretation

---

## 🎯 Design Principles

### Principle 1: Minimize Over-Decomposition
**Bad**: "Compare A vs B" → [Research A, Research B, Compare]  
**Good**: "Compare A vs B" → [Compare A vs B]

### Principle 2: Maximize Parallelization
**Bad**: Sequential when independent  
**Good**: Parallel execution with proper dependency management

### Principle 3: Context is King
Each agent receives:
- Original user prompt (intent)
- Current task description (specific job)
- Previous task results (dependencies only)

### Principle 4: Trust but Verify
- LLM decomposes tasks
- Optimizer validates and improves
- Scheduler ensures execution order
- Database maintains state consistency

---

## 🔄 Execution Lifecycle
![alt text](<architecture/Execution Lifecycle.png>)

---

## 💡 Why This Architecture Works

### Traditional Approach Problems
❌ Blind parallelization breaks dependencies  
❌ Sequential execution is too slow  
❌ Manual orchestration is brittle  
❌ Generic agents lack domain expertise  

### Our Solution Benefits
✅ **Intelligence**: LLM understands task structure  
✅ **Speed**: Parallel execution where possible  
✅ **Reliability**: Dependency management prevents errors  
✅ **Modularity**: Specialized agents for quality  
✅ **Scalability**: Add new agents without changing core logic  

---

## 🎓 Technical Highlights

**1. Subset-Based Scheduling**
```python
if set(task.depends_on).issubset(set(completed)):
    execute(task)
```

**2. Context Injection**
```python
payload = {
    "prompt": task.description,
    "original_prompt": user_input,
    "previous_tasks": get_completed_task_responses(task.depends_on)
}
```

**3. Parallel Batching**
```python
with ThreadPoolExecutor(max_workers=len(ready_tasks)) as executor:
    futures = [executor.submit(send_request, task) for task in ready_tasks]
```

---

## 🔧 Future Enhancements

- [ ] Failure recovery and retry logic
- [ ] Agent result caching
- [ ] Dynamic agent discovery
- [ ] Real-time progress streaming
- [ ] Task priority queues
- [ ] Agent capability negotiation

---

## 📝 Summary

This system demonstrates how **Small Language Models can orchestrate complex workflows** by:
1. Understanding natural language task structure
2. Making intelligent decomposition decisions  
3. Optimizing execution graphs
4. Managing dependencies automatically
5. Maximizing parallelization

The result is a **fast, reliable, and intelligent multi-agent system** that adapts to task complexity while maintaining simplicity where appropriate.