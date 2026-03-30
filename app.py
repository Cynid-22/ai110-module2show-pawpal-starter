import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ==========================================
# STEP 2: Manage the Application "Memory"
# ==========================================
if "SystemOwner" not in st.session_state:
    # Initialize the "vault" with a default Owner and Pet
    InitialOwner = Owner(Name="Jordan", AvailableTime=120)
    InitialOwner.AddPet(Pet(Name="Mochi", Species="cat", Age=3))
    st.session_state.SystemOwner = InitialOwner

st.divider()

# ==========================================
# STEP 3: Wiring UI Actions to Logic
# ==========================================
st.subheader("Manage Pets & Owner")

# Pull active owner references
CurrentOwner = st.session_state.SystemOwner
PrimaryPet = CurrentOwner.Pets[0] if CurrentOwner.Pets else None

OwnerNameInput = st.text_input("Owner name", value=CurrentOwner.Name)
CurrentOwner.UpdateAvailableTime(120) # Default placeholder config
CurrentOwner.Name = OwnerNameInput

if PrimaryPet:
    PetNameInput = st.text_input("Pet name", value=PrimaryPet.Name)
    PetSpeciesInput = st.selectbox("Species", ["dog", "cat", "other"], index=["dog", "cat", "other"].index(PrimaryPet.Species) if PrimaryPet.Species in ["dog", "cat", "other"] else 1)
    # Updating existing pet
    PrimaryPet.UpdateDetails(Name=PetNameInput, Species=PetSpeciesInput, Age=PrimaryPet.Age, SpecialRequirements=str(PrimaryPet.SpecialRequirements))

st.markdown("### Tasks")
st.caption("Add a few tasks. These now directly feed into the PawPal+ backend.")

Col1, Col2, Col3, Col4 = st.columns(4)
with Col1:
    TaskTitleInput = st.text_input("Task title", value="Morning walk")
with Col2:
    TaskDurationInput = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
with Col3:
    TaskPriorityInput = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with Col4:
    TaskTimeInput = st.text_input("Time (e.g. 08:30)", value="08:00")

# Priority text to int mapper
PriorityMap = {"low": 1, "medium": 2, "high": 3}

if st.button("Add task"):
    if PrimaryPet:
        NewBackendTask = Task(
            Description=TaskTitleInput,
            Duration=int(TaskDurationInput),
            PriorityLevel=PriorityMap[TaskPriorityInput],
            Frequency="Daily", # Using Daily default for demo
            TargetPet=PrimaryPet,
            Time=TaskTimeInput
        )
        PrimaryPet.AddTask(NewBackendTask)
        st.success(f"Added {TaskTitleInput} to {PrimaryPet.Name} at {TaskTimeInput}!")
    else:
        st.error("No active pet available to receive tasks.")

# Fetch tasks dynamically from the backend classes
AllSystemTasks = CurrentOwner.GetAllTasks()

if AllSystemTasks:
    # Render table dynamically mapped, invoking the SortByTime function locally for clean tracking
    st.write("Current tasks:")
    EngineForDisplay = Scheduler(SystemOwner=CurrentOwner)
    SortedDisplayTasks = EngineForDisplay.SortByTime(AllSystemTasks)
    
    RenderTableData = [{"Time": T.Time, "Pet": T.TargetPet.Name, "Title": T.Description, "Duration": T.Duration, "Priority": T.PriorityLevel} for T in SortedDisplayTasks]
    st.table(RenderTableData)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
ConfiguredAvailableTime = st.number_input("Available Time Limit (minutes)", min_value=10, max_value=480, value=CurrentOwner.AvailableTime)

if st.button("Generate schedule"):
    CurrentOwner.UpdateAvailableTime(ConfiguredAvailableTime)
    
    # Initialize "Brain" and run the plan
    Engine = Scheduler(SystemOwner=CurrentOwner)
    GeneratedPlan = Engine.GenerateSchedule()
    SortedPlan = Engine.SortByTime(GeneratedPlan)
    
    # Run algorithmic conflict parsing natively through Streamlit Warnings
    Conflicts = Engine.DetectConflicts()
    if Conflicts:
        for Warning in Conflicts:
            st.warning(Warning)
    
    st.success("Schedule logic successfully executed and chronologically sorted!")
    
    TotalTimeSpent = 0
    if SortedPlan:
        PlanData = []
        for ScheduledItem in SortedPlan:
            PlanData.append({
                "Time": ScheduledItem.Time,
                "Task": ScheduledItem.Description,
                "For": ScheduledItem.TargetPet.Name,
                "Duration (min)": ScheduledItem.Duration
            })
            TotalTimeSpent += ScheduledItem.Duration
        st.table(PlanData)
        
    st.info(f"Total time required: {TotalTimeSpent} / {CurrentOwner.AvailableTime} minutes.")
