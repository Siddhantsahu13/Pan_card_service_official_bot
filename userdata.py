# User data management
user_sessions = {}

async def collect_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            'step': 'collecting_name',
            'service_type': '',
            'user_data': {}
        }
    
    current_step = user_sessions[user_id]['step']
    
    if current_step == 'collecting_name':
        user_sessions[user_id]['user_data']['name'] = update.message.text
        user_sessions[user_id]['step'] = 'collecting_dob'
        await update.message.reply_text("📅 Please share your Date of Birth (DD/MM/YYYY):")