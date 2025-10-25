import logging
import json
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# === CONFIGURATION ===
BOT_TOKEN = "8474265926:AAExR2jEP_t7w0HLRbF-B7KE2RVFNu--cJE"  # Step 1 से मिला token यहाँ डालें
ADMIN_ID = "@siddhantsahu570"  # Your personal Telegram ID

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Storage for user data (in production use database)
user_sessions = {}
applications = {}

# === MAIN MENU ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    
    welcome_text = f"""
🟡 **Welcome {user.first_name}!** 🟡

🇮🇳 **PAN CARD SERVICES** 🇮🇳

*Instant PAN Card Solutions at Your Fingertips*

📋 **Our Services:**
├── 🆕 New PAN Card Application
├── ✏️ PAN Correction/Update  
├── 📊 PAN Application Status
├── 💳 Download e-PAN Card
├── 🔍 PAN Verification Service
└── 📞 Premium Support

💎 **Why Choose Us?**
✓ 24-48 Hours Processing
✓ 99% Success Rate
✓ Secure & Confidential
✓ Expert Assistance
✓ Complete Documentation Help

👇 **Select a service below to get started:**
    """
    
    keyboard = [
        [InlineKeyboardButton("🆕 NEW PAN CARD", callback_data="new_pan")],
        [InlineKeyboardButton("✏️ PAN CORRECTION", callback_data="correction")],
        [InlineKeyboardButton("📊 CHECK STATUS", callback_data="status")],
        [InlineKeyboardButton("💳 DOWNLOAD e-PAN", callback_data="download_epan")],
        [InlineKeyboardButton("💰 PRICING", callback_data="pricing"), 
         InlineKeyboardButton("📞 SUPPORT", callback_data="support")],
        [InlineKeyboardButton("ℹ️ ABOUT US", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# === BUTTON HANDLERS ===
async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # ✅ CORRECTED LINE - Proper indentation
    user_id = query.from_user.id
    data = query.data
    
    if data == "new_pan":
        await show_new_pan_options(query)
    elif data == "correction":
        await show_correction_options(query)
    elif data == "pricing":
        await show_pricing_details(query)
    elif data == "support":
        await show_support_info(query)
    elif data == "download_epan":
        await show_download_epan(query)
    elif data == "status":
        await show_status_check(query)
    elif data == "about":
        await show_about_us(query)
    elif data == "main_menu":
        await go_to_main_menu(query)
    elif data.startswith("payment_"):
        await handle_payment_request(query, data)

# === SERVICE FUNCTIONS ===
async def show_new_pan_options(query):
    text = """
🆕 *NEW PAN CARD APPLICATION*

📋 *Required Documents:*
• Aadhaar Card (Mandatory)
• Passport Size Photo
• Signature (White Paper)

🎯 *Processing Time:* 24-48 Hours
💰 *Service Charge:* ₹149 Only

*Select Application Type:*
    """
    
    keyboard = [
        [InlineKeyboardButton("👤 INDIVIDUAL", callback_data="individual_app")],
        [InlineKeyboardButton("🏢 COMPANY/FIRM", callback_data="company_app")],
        [InlineKeyboardButton("📋 DOCUMENT LIST", callback_data="documents_list")],
        [InlineKeyboardButton("🔙 MAIN MENU", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_pricing_details(query):
    text = """
💰 *SERVICE PRICING - TRANSPARENT & AFFORDABLE*

*Basic Services:*
├── 🆕 New PAN Card: *₹149*
├── ✏️ PAN Correction: *₹99*  
├── 💳 Download e-PAN: *₹49*
├── 📊 Status Check: *FREE*
└── 🔍 PAN Verification: *₹29*

*Premium Packages:*
├── 💎 New PAN + Correction: *₹199*
├── 🚀 New PAN + Fast Track: *₹249*
└── 👑 Complete Business Package: *₹499*

*Payment Methods:*
✓ UPI (Google Pay, PhonePe, Paytm)
✓ Bank Transfer
✓ All Debit/Credit Cards

🔒 *100% Refund if Service Not Delivered*
    """
    
    keyboard = [
        [InlineKeyboardButton("🆕 NEW PAN - ₹149", callback_data="payment_new_pan")],
        [InlineKeyboardButton("✏️ CORRECTION - ₹199", callback_data="payment_correction")],
        [InlineKeyboardButton("💳 e-PAN - ₹49", callback_data="payment_epan")],
        [InlineKeyboardButton("📞 CUSTOM QUOTE", callback_data="support")],
        [InlineKeyboardButton("🔙 MAIN MENU", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_support_info(query):
    text = """
📞 *CUSTOMER SUPPORT - WE'RE HERE TO HELP!*

*Quick Contact:*
📧 Email: support@pancardservice.com
📱 WhatsApp: +91-9575016023
🌐 Website: www.pancardservice.com

*Office Hours:*
🕘 9:00 AM - 9:00 PM (Monday-Saturday)
🕚 10:00 AM - 6:00 PM (Sunday)

*Emergency Support:*
For urgent issues, direct call available

*Before Contacting:*
✓ Keep your Application ID ready
✓ Have payment screenshot available
✓ Check status via /start first

👇 *Select your contact method:*
    """
    
    keyboard = [
        [InlineKeyboardButton("📧 SEND EMAIL", url="mailto:support@pancardservice.com")],
        [InlineKeyboardButton("📱 WHATSAPP", url="https://wa.me/91XXXXXXXXXX")],
        [InlineKeyboardButton("📞 CALL SUPPORT", callback_data="call_support")],
        [InlineKeyboardButton("🔙 MAIN MENU", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_payment_request(query, service_type):
    service_price = {
        "payment_new_pan": "₹149",
        "payment_correction": "₹199", 
        "payment_epan": "₹49"
    }
    
    price = service_price.get(service_type, "₹149")
    service_name = service_type.replace("payment_", "").replace("_", " ").title()
    
    text = f"""
💰 *PAYMENT INSTRUCTIONS - {service_name.upper()}*

*Amount to Pay:* {price}

*Payment Method 1 - UPI (Recommended):*
📱 UPI ID: `pancard.service@ybl`

*Payment Method 2 - Bank Transfer:*
🏦 Bank Name: XXX Bank
👤 Account Name: PAN Card Services
🔢 Account Number: XXXX XXXX XXXX
📞 IFSC Code: XXXX012345

*Payment Steps:*
1. Pay {price} using any above method
2. Take screenshot of successful payment
3. Click 'I HAVE PAID' button below
4. Share transaction details with our executive

✅ *After Payment:*
• Executive will contact within 30 minutes
• Document collection started immediately
• 24-48 hours processing time

⚠️ *Important:*
• Mention "PAN Service" in payment note
• Keep transaction ID safe
• Don't share OTP with anyone
    """
    
    keyboard = [
        [InlineKeyboardButton("✅ I HAVE PAID", callback_data="payment_done")],
        [InlineKeyboardButton("📞 PAYMENT HELP", callback_data="support")],
        [InlineKeyboardButton("🔙 MAIN MENU", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Store service type in user session
    user_id = query.from_user.id
    user_sessions[user_id] = {"service_type": service_type, "amount": price}
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_download_epan(query):
    text = """
💳 *DOWNLOAD e-PAN CARD*

*What is e-PAN?*
e-PAN is a digital version of your PAN card, legally valid everywhere.

*Service Features:*
✓ Instant download within 2 hours
✓ Password protected PDF
✓ Digital signature included
✓ Valid for all purposes

*Requirements:*
• PAN Number
• Registered Mobile Number
• Email ID

*Process:*
1. Pay service charge ₹49
2. Share your PAN number
3. Verify via OTP
4. Download e-PAN instantly

👇 *Ready to download your e-PAN?*
    """
    
    keyboard = [
        [InlineKeyboardButton("💳 DOWNLOAD NOW - ₹49", callback_data="payment_epan")],
        [InlineKeyboardButton("📞 NEED HELP?", callback_data="support")],
        [InlineKeyboardButton("🔙 MAIN MENU", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_status_check(query):
    text = """
📊 *CHECK APPLICATION STATUS*

*Track Your PAN Application*

To check your application status, you need:
• Application Reference Number
• Mobile Number used in application

*Status Meanings:*
🟡 Pending - Under process
🟢 Approved - PAN generated  
🔴 Rejected - Check reason
🔵 In Progress - Being processed

👇 *Select option:*
    """
    
    keyboard = [
        [InlineKeyboardButton("🔍 CHECK STATUS", callback_data="check_status_now")],
        [InlineKeyboardButton("📞 STATUS HELP", callback_data="support")],
        [InlineKeyboardButton("🔙 MAIN MENU", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_about_us(query):
    text = """
ℹ️ *ABOUT PAN CARD SERVICES*

*Who We Are?*
We are professional PAN card facilitators with 5+ years experience in document services.

*Our Achievements:*
✓ 10,000+ PAN cards processed
✓ 99% customer satisfaction rate
✓ 24-48 hours average turnaround
✓ Secure & confidential service

*Why Choose Us?*
🔒 **Security First**
Your documents and data are completely secure with us

⚡ **Fast Processing**
Quickest PAN card services in India

💯 **Reliable Service**
99% success rate in application approval

📞 **24/7 Support**
Round the clock customer support

*Legal Compliance:*
We follow all government guidelines and maintain complete transparency in our operations.

*Contact Us:*
📧 Email: info@pancardservice.com
📱 Phone: +91-XXXXXXXXXX
🌐 Website: www.pancardservice.com
    """
    
    keyboard = [
        [InlineKeyboardButton("🆕 GET STARTED", callback_data="new_pan")],
        [InlineKeyboardButton("📞 CONTACT US", callback_data="support")],
        [InlineKeyboardButton("🔙 MAIN MENU", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def go_to_main_menu(query):
    # Create a new update object to pass to start function
    class FakeUpdate:
        def __init__(self, query):
            self.message = type('Message', (), {'from_user': query.from_user})()
            self.message.reply_text = query.edit_message_text
    
    fake_update = FakeUpdate(query)
    await start(fake_update, None)

# === PAYMENT CONFIRMATION ===
async def handle_payment_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user_data = user_sessions.get(user_id, {})
    
    text = """
✅ *PAYMENT CONFIRMED!*

Thank you for your payment! 🎉

*Next Steps:*
1. Our executive will contact you within 30 minutes
2. Please keep your documents ready
3. We'll guide you through document submission
4. Processing will start immediately

*Documents Needed:*
• Aadhaar Card
• Passport Photo
• Signature

*Contact Information:*
📱 WhatsApp: +91-XXXXXXXXXX
📧 Email: support@pancardservice.com

*Application Tracking:*
You'll receive regular updates on your application status.

Thank you for choosing our service! 🙏
    """
    
    keyboard = [
        [InlineKeyboardButton("📞 CONTACT EXECUTIVE", callback_data="support")],
        [InlineKeyboardButton("🏠 MAIN MENU", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    # Send notification to admin
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🆕 New Payment Received!\nUser: {query.from_user.first_name}\nService: {user_data.get('service_type', 'Unknown')}\nAmount: {user_data.get('amount', 'Unknown')}"
    )

# === MESSAGE HANDLER ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text.lower() in ['/start', 'start', 'menu']:
        await start(update, context)
    else:
        await update.message.reply_text(
            "I didn't understand that. Please use the menu buttons or type /start to see available options.",
            parse_mode='Markdown'
        )

# === MAIN FUNCTION ===
def main():
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", start))
    application.add_handler(CallbackQueryHandler(handle_button_click))
    application.add_handler(CallbackQueryHandler(handle_payment_confirmation, pattern="payment_done"))
    
    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    print("🤖 PAN Card Service Bot is starting...")
    print("📍 Bot is now live! Visit: t.me/PancardServiceBot")
    print("🚀 Press Ctrl+C to stop the bot")
    
    application.run_polling()

if __name__ == "__main__":
    main()