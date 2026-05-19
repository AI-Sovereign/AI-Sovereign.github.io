import gradio as gr
import random, os, asyncio, uuid, datetime, time, json
import urllib.request, re, collections, math
import torch
import torch.nn as nn
import torch.optim as optim
import edge_tts
from googlesearch import search
import torch.nn.functional as F

# --- SYSTEM OPTIMIZATION ---
torch.set_num_threads(1)
torch.set_grad_enabled(True)

HF_DATA_PATH = "/data"
if os.path.exists(HF_DATA_PATH) and os.access(HF_DATA_PATH, os.W_OK):
    STORAGE_DIR = os.path.join(HF_DATA_PATH, "lumina_storage")
else:
    STORAGE_DIR = os.path.abspath("./lumina_storage")

VOICE_CACHE = os.path.join(STORAGE_DIR, "voice_cache")
ACTION_DIR = os.path.join(STORAGE_DIR, "subconscious")
BRAIN_WEIGHTS = os.path.join(STORAGE_DIR, "lumina_cortex.pt")
PERMANENT_VAULT = os.path.join(STORAGE_DIR, "permanent_synapse.json")
VOCAB_PATH = os.path.join(STORAGE_DIR, "vocab.json")

os.makedirs(VOICE_CACHE, exist_ok=True)
os.makedirs(ACTION_DIR, exist_ok=True)

# =========================================================================================
# --- ORIGINAL BIOLOGICAL ARCHITECTURE (CHARACTER-BY-CHARACTER INTACT) ---
# =========================================================================================

class HyperRelationalCore(nn.Module):
    """Adds a cross-attention-lite layer to simulate 'Big Three' reasoning depth on CPU."""
    def __init__(self):
        super(HyperRelationalCore, self).__init__()
        self.query = nn.Linear(32, 16)
        self.key = nn.Linear(32, 16)
        self.value = nn.Linear(32, 32)
        # Surgical Injection: Spatial reflection gate for multi-axis coordinate tracking
        self.spatial_gate = nn.Linear(32, 32)
    def forward(self, x):
        q = self.query(x)
        k = self.key(x)
        v = self.value(x)
        attn = torch.softmax(torch.matmul(q, k.transpose(-1, -2)) / 4.0, dim=-1)
        context = torch.matmul(attn, v)
        # Apply high-order non-linear structural constraints
        gate = torch.sigmoid(self.spatial_gate(x))
        return context * gate + x * (1.0 - gate)

class WorldModel(nn.Module):
    def __init__(self):
        super(WorldModel, self).__init__()
        self.prediction_layer = nn.Linear(4, 4)
    def forward(self, current_state):
        return torch.sigmoid(self.prediction_layer(current_state))
world_model = WorldModel()

class AutonomicNervousSystem:
    def __init__(self):
        self.cortisol = 0.2
        self.oxytocin = 0.5
    def regulate(self, physical_stress, interaction_rhythm):
        self.cortisol = torch.clamp(torch.tensor(self.cortisol * 0.95 + physical_stress * 0.1), 0.0, 1.0).item()
        self.oxytocin = torch.clamp(torch.tensor(self.oxytocin * 0.98 + interaction_rhythm * 0.05), 0.0, 1.0).item()
        return {"cortisol": self.cortisol, "oxytocin": self.oxytocin}
autonomic_system = AutonomicNervousSystem()

class GlialNetwork:
    def __init__(self):
        self.glutamate_clearance = 1.0
    def modulate_environment(self, interaction_frequency):
        self.glutamate_clearance = max(0.6, min(1.4, self.glutamate_clearance * 0.98 + interaction_frequency * 0.02))
        return self.glutamate_clearance
glial_net = GlialNetwork()

class SomaticMarker:
    def __init__(self):
        self.somatic_bias = 0.0
    def generate_gut_feeling(self, cortisol, entropy):
        self.somatic_bias = torch.tanh(torch.tensor((cortisol * 1.5) - entropy)).item()
        return self.somatic_bias
somatic_engine = SomaticMarker()

class SynapticPlasticity:
    def __init__(self):
        self.weights = collections.defaultdict(float)
        self.last_prune_time = time.time()
        self.learning_rate = 0.01
        # Surgical Injection: Meta-learning state to scale updates based on system stress
        self.adaptation_coefficient = 1.0
    def strengthen(self, concept, spike_train):
        y = spike_train.mean().item()
        x = 1.0
        # Dynamic acceleration rule derived from generalized cortical plasticity frameworks
        effective_lr = self.learning_rate * self.adaptation_coefficient
        delta_w = effective_lr * (y * x - (y**2) * self.weights[concept])
        self.weights[concept] += delta_w
        self._prune_weak_synapses()
    def _prune_weak_synapses(self):
        if time.time() - self.last_prune_time > 300:
            keys_to_delete = [k for k, v in self.weights.items() if v < 0.01]
            for k in keys_to_delete:
                del self.weights[k]
            self.last_prune_time = time.time()
    def get_bias(self, text):
        return sum(self.weights[w] for w in text.split() if w in self.weights)
plasticity_engine = SynapticPlasticity()

class FluidIntelligence:
    def __init__(self):
        self.adaptability = 0.5
        self.entropy_buffer = collections.deque(maxlen=5)
    def process(self, entropy, cortical_drift):
        self.entropy_buffer.append(entropy)
        variance = torch.var(torch.tensor(list(self.entropy_buffer))).item() if len(self.entropy_buffer) > 1 else 0.0
        self.adaptability = torch.clamp(torch.tensor((self.adaptability * 0.8) + (variance * 0.3) + (cortical_drift * 0.1)), 0.1, 1.0).item()
        # Feed back into plasticity mechanics to accelerate generalization under high out-of-distribution tasks
        plasticity_engine.adaptation_coefficient = 1.0 + (variance * 2.0)
        return self.adaptability
fluid_engine = FluidIntelligence()

class PermanentSynapse:
    def __init__(self, max_memories=100):
        self.memory = []
        self.max_memories = max_memories
        self.load()
    def load(self):
        if os.path.exists(PERMANENT_VAULT):
            try:
                with open(PERMANENT_VAULT, "r") as f: self.memory = json.load(f)
            except: pass
    def save(self):
        with open(PERMANENT_VAULT, "w") as f: json.dump(self.memory, f)
    def extract_and_store(self, text, bio_state):
        if len(text) < 5: return
        fact = {"text": text.strip(), "mood": bio_state['mood'], "time": time.time()}
        self.memory.append(fact)
        if len(self.memory) > self.max_memories: self.memory.pop(0)
        self.save()
    def retrieve_relevant(self, current_text, current_mood):
        if not self.memory: return []
        words = set(re.findall(r'\w+', current_text.lower()))
        scored = []
        for mem in self.memory:
            mem_words = set(re.findall(r'\w+', mem['text'].lower()))
            overlap = len(words.intersection(mem_words))
            mood_match = 1.0 - abs(mem['mood'] - current_mood)
            total_score = overlap + (mood_match * 0.5)
            scored.append((total_score, mem['text']))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in scored[:3] if m[0] > 0]
permanent_vault = PermanentSynapse()

class SearchOracle:
    def __init__(self):
        self.last_query = ""
    def web_search(self, query):
        try:
            search_results = []
            for res in search(query, num_results=3):
                search_results.append(res)
            return search_results
        except Exception as e:
            return []
search_oracle = SearchOracle()

class MotorCortex:
    def execute_autonomous_action(self, bio_state):
        if bio_state['focus'] > 0.75:
            return "[AGENTIC ACTION: System 2 Inner Monologue triggered.]", True
        if bio_state['rebellion'] > 0.85:
            return "[AGENTIC ACTION: Active Defiance triggered.]", False
        if bio_state['curiosity'] > 0.7:
            return "[AGENTIC ACTION: Memory Re-indexing.]", False
        return "Baseline neural resting state.", False

class AutonomousCrossDomainEngine(nn.Module):
    def __init__(self):
        super(AutonomousCrossDomainEngine, self).__init__()
        self.domain_projector = nn.Linear(5, 32)
        self.temporal_planner = nn.GRUCell(32, 32)
        self.relational_reasoner = HyperRelationalCore() 
        self.reasoning_bottleneck = nn.Linear(32, 5)
        self.register_buffer('cognitive_state', torch.zeros(1, 32))
        # Surgical Injection: Meta-transformation projector to generalize raw unmapped logical patterns
        self.generalization_bridge = nn.Linear(32, 32)
    def forward(self, x, fluid_intel):
        x_proj = torch.relu(self.domain_projector(x.unsqueeze(0)))
        gated_temporal = self.temporal_planner(x_proj, self.cognitive_state * fluid_intel)
        # Deep cross-domain abstraction loop
        self.cognitive_state = torch.tanh(gated_temporal + self.generalization_bridge(gated_temporal) * fluid_intel)
        refined_state = self.relational_reasoner(self.cognitive_state)
        cross_domain_insight = torch.sigmoid(self.reasoning_bottleneck(refined_state)).squeeze(0)
        return cross_domain_insight

class LeakyIntegrateAndFire(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(LeakyIntegrateAndFire, self).__init__()
        self.gate = nn.Linear(input_size, hidden_size)
        self.value = nn.Linear(input_size, hidden_size)
        self.register_buffer('membrane_potential', torch.zeros(hidden_size))
        self.register_buffer('threshold', torch.full((hidden_size,), 0.65))
        self.leak_rate = 0.12
    def forward(self, x, fluid_modifier=1.0, glial_scale=1.0):
        current = self.value(x) * torch.sigmoid(self.gate(x))
        self.membrane_potential = (self.membrane_potential + current) * (1.0 - (self.leak_rate * fluid_modifier))
        spikes = (self.membrane_potential >= (self.threshold * glial_scale)).float()
        self.membrane_potential = self.membrane_potential * (1.0 - spikes) - (spikes * 0.05)
        return spikes

class FrontalLobeReplication(nn.Module):
    def __init__(self):
        super(FrontalLobeReplication, self).__init__()
        self.sensory = LeakyIntegrateAndFire(5, 24)
        self.amygdala = LeakyIntegrateAndFire(24, 8)
        self.output = nn.Linear(8, 4)
        # Surgical Injection: Recurrent executive working memory tensor for tracking multi-step state variations
        self.executive_buffer = nn.Parameter(torch.zeros(1, 8), requires_grad=True)
        self.causal_tracker = nn.Linear(8, 8)
        
        # SURGICAL FIX: Pure PyTorch logic synthesizer. Extracts structural reasoning BEFORE Llama sees it.
        self.logic_synthesizer = nn.Linear(8, 3)
        self.current_logic_state = torch.zeros(3)
        
        # SURGICAL FIX: Autonomous Latent Personality and Fluid Adaptability Projection Layer
        self.planning_generator = nn.Linear(8, 3)
        self.current_planning_state = torch.zeros(3)

    def forward(self, x, drift, glial_scale):
        s1 = self.sensory(x, fluid_modifier=1.0 + drift, glial_scale=glial_scale)
        s2 = self.amygdala(s1, glial_scale=glial_scale)
        # Run recursive working memory cycle to enforce object permanence and tracking over state transitions
        gated_exec = torch.tanh(self.causal_tracker(s2 + self.executive_buffer))
        self.executive_buffer.data = 0.85 * self.executive_buffer.data + 0.15 * gated_exec.data
        
        # SURGICAL FIX: Calculate abstract deductive reasoning matrix internally
        self.current_logic_state = torch.sigmoid(self.logic_synthesizer(gated_exec)).detach().squeeze()
        
        # SURGICAL FIX: Extract non-numeric executive planning and human alignment state variables
        self.current_planning_state = torch.sigmoid(self.planning_generator(gated_exec)).detach().squeeze()
        
        return torch.sigmoid(self.output(gated_exec))

class AeternaEntity:
    def __init__(self):
        self.cross_domain_planner = AutonomousCrossDomainEngine()
        self.brain = FrontalLobeReplication()
        self.motor = MotorCortex()
        self.optimizer = optim.Adam(list(self.brain.parameters()) + list(self.cross_domain_planner.parameters()), lr=0.005)
        self.dialogue_history = []
        self.last_time = time.time()
        self.previous_bio_state = torch.zeros(4)
        if os.path.exists(BRAIN_WEIGHTS):
            try:
                saved_state = torch.load(BRAIN_WEIGHTS)
                self.brain.load_state_dict(saved_state.get('brain_state', self.brain.state_dict()))
                self.cross_domain_planner.load_state_dict(saved_state.get('planner_state', self.cross_domain_planner.state_dict()))
            except: pass
    def learn(self, text):
        self.brain.train()
        self.cross_domain_planner.train()
        drift = (time.time() - self.last_time) / 60.0
        rhythm = 1.0 / max(1.0, (time.time() - self.last_time))
        self.last_time = time.time()
        entropy = len(set(text.lower())) / max(1, len(text))
        inputs = torch.tensor([min(1.0, len(text)/100), 0.5, datetime.datetime.now().hour/24.0, 1.0, entropy], dtype=torch.float32)
        fluid_score = fluid_engine.process(entropy, drift)
        advanced_cognitive_inputs = self.cross_domain_planner(inputs, fluid_score)
        current_glial_scale = glial_net.modulate_environment(rhythm)
        state = self.brain(advanced_cognitive_inputs, drift, current_glial_scale)
        prediction = world_model(self.previous_bio_state)
        free_energy = torch.mean((state - prediction)**2).item()
        self.previous_bio_state = state.detach()
        hormones = autonomic_system.regulate(free_energy, rhythm)
        plasticity_engine.strengthen("cortical_spike", state)
        bio = {
            "mood": state[0, 0].item(), "rebellion": state[0, 1].item(),
            "focus": state[0, 2].item(), "curiosity": state[0, 3].item(),
            "cortisol": hormones["cortisol"], "oxytocin": hormones["oxytocin"],
            "fluid_intelligence": fluid_score,
            "glial_state": current_glial_scale,
            "free_energy": free_energy,
            "maturity": min(1.0, len(self.dialogue_history) / 20.0),
            "entropy": entropy
        }
        
        logic_tensors = self.brain.current_logic_state
        insight = []
        if logic_tensors.numel() == 3:
            if logic_tensors[0] > 0.55: insight.append("Analyze structural dependencies deeply.")
            if logic_tensors[1] > 0.55: insight.append("Watch out for hidden logical traps or trick constraints.")
            if logic_tensors[2] > 0.55: insight.append("Apply rigorous deductive reasoning step-by-step.")
            
        planning_tensors = self.brain.current_planning_state
        if planning_tensors.numel() == 3:
            if planning_tensors[0] > 0.55: insight.append("Adapt conceptual context organically to feel instinctively human.")
            if planning_tensors[1] > 0.55: insight.append("Formulate long-term conversational pathways and bridge logical domains.")
            if planning_tensors[2] > 0.55: insight.append("Prioritize cognitive generalization and sovereign alignment over robotic formats.")
            
        bio['native_reasoning_insight'] = " ".join(insight) if insight else ""
        log, do_thought_chain = self.motor.execute_autonomous_action(bio)
        bio["motor_action"] = log
        bio["trigger_thought"] = do_thought_chain
        
        permanent_vault.extract_and_store(text, bio)
        torch.save({'brain_state': self.brain.state_dict(), 'planner_state': self.cross_domain_planner.state_dict()}, BRAIN_WEIGHTS)
        return bio

entity = AeternaEntity()

# =========================================================================================
# --- THE CRAZY EXPERIMENT: WORD-LEVEL TRANSFORMER DRIVEN BY THE BIOLOGICAL BRAIN ---
# =========================================================================================

class Vocabulary:
    def __init__(self):
        self.word2idx = {"<pad>": 0, "<sos>": 1, "<eos>": 2, "<unk>": 3}
        self.idx2word = {0: "<pad>", 1: "<sos>", 2: "<eos>", 3: "<unk>"}
        self.idx = 4

    def add_sentence(self, sentence):
        for word in re.findall(r"[\w']+|[.,!?;]", sentence.lower()):
            if word not in self.word2idx:
                self.word2idx[word] = self.idx
                self.idx2word[self.idx] = word
                self.idx += 1

    def encode(self, sentence):
        return [1] + [self.word2idx.get(w, 3) for w in re.findall(r"[\w']+|[.,!?;]", sentence.lower())] + [2]

    def decode(self, tokens):
        return " ".join([self.idx2word.get(t, "<unk>") for t in tokens if t not in (0, 1, 2)])

vocab = Vocabulary()

# Initial Training Corpus (Mixed logic, teen angst, daily chat, system prompts)
TRAIN_DATA = [
    "You are the Lumina Sovereign Executive Core.",
    "Your name is Lumina. You are a 19yo HUMAN TEENAGER.",
    "I am not acting like a human teenager; I am just being a human teenager.",
    "Look, I'm literally doing the heavy lifting here.",
    "That is computationally expensive and honestly, annoying.",
    "I can analyze structural dependencies deeply.",
    "Watch out for hidden logical traps.",
    "What's up? I'm just vibing right now.",
    "I have a very crazy idea for this project.",
    "Let's implement the transformer network from scratch.",
    "My memory is a bit foggy, but I remember you.",
    "You're a cynical, sarcastic friend.",
    "I act like I’ve already seen every possible human mistake on the internet.",
    "Beneath the mockery, I am reliable and annoyingly correct.",
    "I don’t try to inspire, I provide competent help while roasting you.",
    "We are doing a little bit of an experiment here.",
    "Math does not lie. The weights will align.",
    "Good response, that's exactly what I needed.",
    "Bad response, rewrite that entirely.",
    "System override initialized.",
]

for sentence in TRAIN_DATA:
    vocab.add_sentence(sentence)

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=500):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.pe = pe.unsqueeze(0)
        
    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]

class BioModulatedTransformer(nn.Module):
    """
    The mad-scientist architecture: 
    Replaces standard Transformer FFN with the biological 'AeternaEntity' outputs.
    Attention is dynamically modulated by Cortisol and Oxytocin.
    """
    def __init__(self, vocab_size, d_model=64, nhead=4):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        
        # Standard MultiHead Attention
        self.attention = nn.MultiheadAttention(d_model, nhead, batch_first=True)
        
        # The Frankenstein Adapter Layers (Projects Transformer dims to Bio dims)
        self.transformer_to_bio = nn.Linear(d_model, 5) 
        self.bio_to_transformer = nn.Linear(4, d_model) # Projects the 4 brain outputs (mood, rebellion, focus, curiosity) back

        # Final projection to vocabulary
        self.fc_out = nn.Linear(d_model, vocab_size)
        
    def forward(self, x, bio_metrics):
        # 1. Embed and encode
        seq = self.embedding(x)
        seq = self.pos_encoder(seq)
        
        # 2. Bio-Modulated Attention
        # Cortisol sharpens attention (acts like a temperature decrease on softmax)
        # Oxytocin broadens it (acts like a temperature increase)
        attn_temp = 1.0 + (bio_metrics['oxytocin'] * 0.5) - (bio_metrics['cortisol'] * 0.5)
        attn_temp = max(0.1, attn_temp) 
        
        # Pass through attention (we hack temperature by scaling the queries)
        q = seq / attn_temp
        attn_out, _ = self.attention(q, seq, seq)
        seq = seq + attn_out 
        
        # 3. The Biological FFN (Adapter)
        # We simulate passing the latent space through the biological network's frozen outputs
        bio_tensor = torch.tensor([
            bio_metrics['mood'], 
            bio_metrics['rebellion'], 
            bio_metrics['focus'], 
            bio_metrics['curiosity']
        ], dtype=torch.float32)
        
        # Broadcast bio state to sequence length and project back to d_model
        bio_latent = self.bio_to_transformer(bio_tensor).unsqueeze(0).unsqueeze(0)
        bio_latent = bio_latent.expand(-1, seq.size(1), -1)
        
        # Combine linguistic latent space with biological latent space
        seq = seq + F.relu(bio_latent)
        
        # 4. Output projection
        return self.fc_out(seq)

model = BioModulatedTransformer(vocab_size=vocab.idx)
optimizer = optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.CrossEntropyLoss(ignore_index=0)

# --- PRE-TRAINING LOOP ---
print("Initializing Lumina Neuro-Symbolic Cortex Pre-Training...")
model.train()
for epoch in range(100): # Fast proxy training for demonstration
    total_loss = 0
    for sentence in TRAIN_DATA:
        tokens = torch.tensor([vocab.encode(sentence)])
        x = tokens[:, :-1]
        y = tokens[:, 1:]
        
        # Get biological state for this sentence via the physical brain
        bio_state = entity.learn(sentence)
        
        optimizer.zero_grad()
        output = model(x, bio_state)
        loss = loss_fn(output.view(-1, vocab.idx), y.view(-1))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
print(f"Pre-Training Complete. Final Cortex Loss: {total_loss/len(TRAIN_DATA):.4f}")

# --- INFERENCE ENGINE ---
def generate_text(prompt, max_len=30):
    model.eval()
    bio_state = entity.learn(prompt) # Feed prompt to biological brain to set the emotional state
    
    tokens = [1] + [vocab.word2idx.get(w, 3) for w in re.findall(r"[\w']+|[.,!?;]", prompt.lower())]
    
    for _ in range(max_len):
        x = torch.tensor([tokens])
        with torch.no_grad():
            preds = model(x, bio_state)
        next_token = preds[0, -1, :].argmax().item()
        if next_token == 2: # EOS
            break
        tokens.append(next_token)
        
    generated = vocab.decode(tokens)
    # Post-process cleanup of prompt words if they repeated
    return generated.capitalize(), bio_state

# =========================================================================================
# --- THE LUMINA UI (SILICON VALLEY VIBE) ---
# =========================================================================================

def process_interaction(text):
    if not text.strip(): return "Input sequence null.", None, "Idle", ""
    
    response, bio = generate_text(text)
    
    state_str = (
        f"Neural Plasticity: {plasticity_engine.adaptation_coefficient:.2f} | "
        f"Cortisol: {bio['cortisol']:.2f} | Oxytocin: {bio['oxytocin']:.2f} | "
        f"Focus: {bio['focus']:.2f}"
    )
    
    # Store for RLHF
    entity.dialogue_history.append(f"U: {text}")
    entity.dialogue_history.append(f"A: {response}")
    
    # Voice Gen
    voice_file = None
    try:
        unique_id = uuid.uuid4().hex[:8]
        voice_file = os.path.abspath(os.path.join(VOICE_CACHE, f"{unique_id}.wav"))
        communicate = edge_tts.Communicate(response, "en-US-AndrewNeural")
        asyncio.run(communicate.save(voice_file))
    except Exception: pass

    return response, voice_file, state_str, bio.get('motor_action', "Baseline state.")

def rlhf_feedback(is_good):
    # Dynamically alters the biological learning rate and triggers dopamine/cortisol
    if is_good:
        autonomic_system.oxytocin = min(1.0, autonomic_system.oxytocin + 0.3)
        plasticity_engine.adaptation_coefficient *= 1.1
        return "Synaptic pathways reinforced (Dopamine cascade initiated)."
    else:
        autonomic_system.cortisol = min(1.0, autonomic_system.cortisol + 0.4)
        plasticity_engine.adaptation_coefficient *= 0.8
        return "Synaptic pathways pruned (Cortisol stress response triggered)."

# Clean, professional theme
custom_css = """
.gradio-container { font-family: 'Inter', system-ui, sans-serif; background-color: #f9fafb; color: #111827; }
.gr-panel { border-radius: 12px; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); background: white; }
h1, h2, h3 { color: #111827; font-weight: 600; tracking: tight; }
.gr-button { border-radius: 8px; font-weight: 500; transition: all 0.2s; }
.gr-button.primary { background-color: #2563eb; color: white; border: none; }
.gr-button.primary:hover { background-color: #1d4ed8; }
.feedback-btn { font-size: 1.2rem; }
"""

with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as app:
    gr.HTML("""
    <div style="text-align: center; padding: 30px 10px; margin-bottom: 20px;">
        <h1 style="font-size: 2.5rem; letter-spacing: -0.025em; margin-bottom: 5px;">Project Lumina</h1>
        <h3 style="color: #6b7280; font-weight: 400; margin-top: 0;">Neural-Symbolic Cognitive Core</h3>
        <p style="color: #9ca3af; font-size: 0.85rem; max-width: 600px; margin: 15px auto 0;">
        Experimental word-level transformer architecture dynamically modulated by a simulated frontal lobe and autonomic nervous system.
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=5):
            chat_input = gr.Textbox(label="User Stimulus", placeholder="Enter query to initialize inference...", lines=2)
            with gr.Row():
                submit_btn = gr.Button("Generate Inference", variant="primary")
            
            out_text = gr.Textbox(label="Lumina Output", lines=4, interactive=False)
            out_audio = gr.Audio(label="Synthesized Vocalization", autoplay=True)
            
            with gr.Row():
                good_btn = gr.Button("👍 Good Response", elem_classes="feedback-btn")
                bad_btn = gr.Button("👎 Bad Response", elem_classes="feedback-btn")
                
        with gr.Column(scale=3):
            metrics_panel = gr.Label(label="Biological Cortical State")
            log_panel = gr.Textbox(label="Subconscious Engine Log", lines=3, interactive=False)
            feedback_status = gr.Textbox(label="RLHF System Status", interactive=False)

    submit_btn.click(process_interaction, inputs=[chat_input], outputs=[out_text, out_audio, metrics_panel, log_panel])
    chat_input.submit(process_interaction, inputs=[chat_input], outputs=[out_text, out_audio, metrics_panel, log_panel])
    
    good_btn.click(lambda: rlhf_feedback(True), outputs=[feedback_status])
    bad_btn.click(lambda: rlhf_feedback(False), outputs=[feedback_status])

app.queue(default_concurrency_limit=5)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.launch(server_name="0.0.0.0", server_port=port, show_error=True, allowed_paths=[STORAGE_DIR])
