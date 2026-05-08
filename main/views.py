from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import AdminLoginForm, AdminProfileForm, LeadRequestForm
from .models import LeadRequest, UserProfile

ADVICE_ARTICLES = {
    'care-gold-silver-shine': {
        'title': 'Искусство заботы: Как сохранить блеск ваших золотых и серебряных украшений на долгие годы',
        'lead': 'От чистого золота до серебра — гид по чистке ваших украшений, чтобы свести к минимуму необходимость в глубокой чистке',
        'image': 'main/img/tips_page/photo1.png',
        'gold_section': {
            'title': 'Золотые украшения (585, 750 проба и другие)',
            'image': 'main/img/advice_single_page/section_1_photo.png',
            'intro': (
                'Золото — благородный, но относительно мягкий металл. Современные сплавы делают его прочнее, '
                'но основные правила ухода остаются неизменными.'
            ),
            'enemy_items': [
                'Химия: Косметика, парфюм, кремы, лаки для волос, бытовая химия.',
                'Механические повреждения: Трение, удары, контакт с более твердыми материалами.',
                'Влага и пот: Постоянное ношение в душе, бассейне, спортзале.',
            ],
        },
        'rules_clean_section': {
            'left_title': 'Правила ежедневного ношения:',
            'right_title': 'Как чистить золото в домашних условиях:',
            'left_items': [
                '«Украшения — в последнюю очередь». Надевайте их после того, как нанесли макияж, лосьон и духи.',
                '«Снимайте — в первую очередь». Снимайте перед уборкой, спортом, принятием ванны, походом в сауну или бассейн (хлор агрессивен).',
                'Аккуратность. Избегайте контакта с абразивными поверхностями. Цепочки и браслеты легко поцарапать.',
                'Хранение поодиночке. Храните каждое украшение отдельно, чтобы они не царапали друг друга. Идеально — в шкатулке с мягкими отделениями или в индивидуальных мешочках/коробочках.',
            ],
            'right_items': [
                'Мягкий способ: Теплый мыльный раствор (используйте мягкое мыло без агрессивных ПАВ) + мягкая зубная щетка. Аккуратно почистите щеткой, смойте под проточной водой, вытрите насухо мягкой безворсовой салфеткой (например, из микрофибры).',
                'Для украшений без камней (особенно матовых): Можно ненадолго замочить в растворе средства для мытья посуды.',
                'Важно: Не используйте этот метод для украшений с жемчугом, кораллом, янтарем, малахитом, эмалью или непрозрачными вставками (бирюза, опал).',
            ],
        },
        'silver_section': {
            'title': 'Серебряные украшения (925 проба — стерлинговое серебро)',
            'image': 'main/img/advice_single_page/section_2_photo.png',
            'intro': (
                'Серебро — более активный металл, и его главный враг — окисление, которое проявляется '
                'в виде темного налета (сульфидного слоя).'
            ),
            'enemies_label': 'Основные враги серебра:',
            'enemy_items': [
                'Химические вещества: Та же бытовая химия, сера в некоторых минеральных водах и продуктах (яйца, лук).',
                'Неправильное хранение: Влажная среда, открытый воздух.',
                (
                    'Сера и влага: При контакте с воздухом, содержащим сероводород (есть в городской атмосфере), '
                    'серебро темнеет. Ускоряет процесс высокая влажность.'
                ),
            ],
            'wear_title': 'Правила ежедневного ношения:',
            'wear_items': [
                (
                    'Носите чаще! Лучшая профилактика потемнения — постоянный контакт с кожей. Кожный жир создает '
                    'естественную защитную пленку.'
                ),
                'Те же правила, что и для золота: снимать перед контактом с химией, водой и спортом.',
                'Быстрая сушка. Если серебро намокло, сразу вытрите его насухо.',
            ],
            'clean_title': 'Как чистить золото в домашних условиях:',
            'clean_items': [
                (
                    'Профилактика: Храните серебро в закрытых шкатулках, можно положить внутрь специальную '
                    'антиоксидантную салфетку или мешочек с силикагелем, поглощающим влагу.'
                ),
                'Мягкая чистка: Подойдет тот же мыльный раствор и мягкая щетка.',
                'Чистка содой (для изделий без чернения, камней и эмали):',
                'Специальные средства: Ювелирные салфетки для чистки или жидкие составы. Следуйте инструкции.',
            ],
        },
        'special_cases_section': {
            'title': 'Особые случаи и общие запреты',
            'stones_heading': 'Украшения с камнями (бриллианты, изумруды, сапфиры и др.):',
            'stones_paragraphs': [
                'Бриллианты со временем могут «засаливаться» из-за жира. Чистите мыльным раствором и щеткой.',
                (
                    'Изумруды, опалы, жемчуг, кораллы — пористые и нежные. Только мягкая влажная салфетка, '
                    'никакого замачивания и агрессивной химии.'
                ),
                'Фианиты, топазы, гранаты — более устойчивы, но требуют аккуратности.',
            ],
            'ban_heading': 'Общие правила, которые нарушать нельзя:',
            'ban_paragraphs': [
                (
                    'НИКОГДА не чистите украшения зубной пастой или порошком. Это абразивы, они оставят '
                    'микроцарапины.'
                ),
                (
                    'НИКОГДА не используйте для чистки хлор, нашатырный спирт, уксус '
                    '(кроме особых случаев с серебром) и другую агрессивную химию.'
                ),
                'Не храните украшения в ванной — это самое влажное место в доме.',
                'Не пытайтесь «отполировать» украшения жесткой стороной губки для мытья посуды.',
            ],
            'pro_image': 'main/img/advice_single_page/section_3_photo.png',
            'pro_heading': 'Когда пора к профессионалу:',
            'pro_paragraphs': [
                'Украшение сильно поцарапано, потускнело и домашняя чистка не помогает.',
                'Вы сомневаетесь в безопасности метода для конкретного камня или покрытия.',
                (
                    'Появились сомнения в целостности изделия: расшатались касты, ослабла застежка, '
                    'есть подозрительный изгиб.'
                ),
                (
                    'Ювелир проведет профессиональную ультразвуковую или паровую чистку, выполнит полировку '
                    'и ремонт.'
                ),
            ],
        },
    },
    'clean-dark-spots-fast': {
        'title': 'Верните блеск за минуту: Как безопасно удалить темные пятна с цепочек и звеньев',
        'lead': 'Пошаговая инструкция по чистке труднодоступных мест на цепочках, браслетах-панцирях и ажурных серьгах, где чаще всего скапливается грязь.',
        'image': 'main/img/tips_page/photo2.png',
    },
    'ultrasound-myths': {
        'title': 'Ультразвуковая ванна дома: Правда и мифы о профессиональных средствах чистки',
        'lead': 'Какие украшения можно и нельзя чистить ультразвуком, как выбрать раствор и избежать роковых ошибок при домашнем использовании.',
        'image': 'main/img/tips_page/photo3.png',
    },
    'buy-guide-1': {
        'title': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
        'lead': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore.',
        'image': 'main/img/tips_page/photo1.png',
    },
    'buy-guide-2': {
        'title': 'Lorem ipsum dolor sit amet, consectetur',
        'lead': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut enim ad minim veniam.',
        'image': 'main/img/tips_page/photo2.png',
    },
    'buy-guide-3': {
        'title': 'Lorem ipsum dolor sit amet',
        'lead': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis aute irure dolor in reprehenderit.',
        'image': 'main/img/tips_page/photo3.png',
    },
}

ADVICE_DETAILS_TEXT = {
    'info_title': 'Информация',
    'info_text': 'Ювелирные украшения из золота и серебра — это не просто аксессуары. Это хранители воспоминаний, символы любви и семейные реликвии, которые могут передаваться из поколения в поколение. Но чтобы они сияли так же ярко, как в день покупки, им нужен грамотный уход. Мы собрали полное руководство, которое поможет вам сохранить красоту ваших сокровищ.',
    'footer_text': 'Помните: ваши украшения достойны такого же бережного отношения, как и те драгоценные моменты, с которыми они связаны. Пусть они сияют на вас долгие годы!',
}


def home(request):
    return render(request, 'main/index.html')


def privacy_policy(request):
    return render(request, 'main/privacy-policy.html')


def public_offer(request):
    return render(request, 'main/public-offer.html')


def contacts(request):
    if request.method == 'POST':
        form = LeadRequestForm(request.POST)
        if form.is_valid():
            form.save(LeadRequest.SOURCE_CONTACTS)
            messages.success(request, 'Заявка отправлена! Мы скоро с вами свяжемся.')
        else:
            messages.error(request, 'Проверьте поля формы и попробуйте снова.')
        return redirect('contacts')
    return render(request, 'main/contacts.html')


def about(request):
    if request.method == 'POST':
        form = LeadRequestForm(request.POST)
        if form.is_valid():
            form.save(LeadRequest.SOURCE_ABOUT)
            messages.success(request, 'Заявка отправлена! Мы скоро с вами свяжемся.')
        else:
            messages.error(request, 'Проверьте поля формы и попробуйте снова.')
        return redirect('about')
    return render(request, 'main/about.html')


def services(request):
    if request.method == 'POST':
        form = LeadRequestForm(request.POST)
        if form.is_valid():
            form.save(LeadRequest.SOURCE_SERVICES)
            messages.success(request, 'Заявка отправлена! Мы скоро с вами свяжемся.')
        else:
            messages.error(request, 'Проверьте поля формы и попробуйте снова.')
        return redirect('services')
    return render(request, 'main/services.html')


def author_jewelry(request):
    if request.method == 'POST':
        question = (request.POST.get('question') or '').strip()
        material = (request.POST.get('material') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        consent = request.POST.get('consent')

        if question and material and phone and consent:
            LeadRequest.objects.create(
                source=LeadRequest.SOURCE_AUTHOR_JEWELRY,
                question=f'Описание украшения: {question}\nМатериал/камень: {material}',
                phone=phone,
            )
            messages.success(request, 'Заявка отправлена! Мы скоро с вами свяжемся.')
        else:
            messages.error(request, 'Проверьте поля формы и попробуйте снова.')
        return redirect('author_jewelry')

    return render(request, 'main/author-jewelry.html')


def advices(request):
    return render(request, 'main/advices.html')


def advice_detail(request, slug):
    article = ADVICE_ARTICLES.get(slug)
    if not article:
        raise Http404()
    context = {
        'article': article,
        'article_info': ADVICE_DETAILS_TEXT,
    }
    return render(request, 'main/advice-detail.html', context)


def admin_panel_entry(request):
    if request.user.is_authenticated:
        return redirect('admin_profile')
    return redirect('admin_login')


def ensure_default_admin():
    user_model = get_user_model()
    if not user_model.objects.filter(username='admin').exists():
        user_model.objects.create_user(
            username='admin',
            password='admin12345',
            first_name='Администратор',
            email='admin@example.com',
        )


def admin_login(request):
    ensure_default_admin()

    if request.user.is_authenticated:
        return redirect('admin_profile')

    form = AdminLoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('admin_profile')

    return render(request, 'main/admin/login.html', {'form': form})


@login_required(login_url='admin_login')
def admin_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = AdminProfileForm(request.POST, request.FILES)
        if form.is_valid():
            password_changed = bool(form.cleaned_data.get('password'))
            form.save(request.user)
            if password_changed:
                logout(request)
                messages.success(request, 'Пароль обновлен. Войдите снова.')
                return redirect('admin_login')
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('admin_profile')
    else:
        form = AdminProfileForm(
            initial={
                'first_name': request.user.first_name,
                'email': request.user.email,
            }
        )

    return render(
        request,
        'main/admin/profile.html',
        {
            'form': form,
            'profile': profile,
        },
    )


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


def custom_404(request, exception):
    return render(request, 'main/404.html', status=404)


def custom_404_debug(request, unknown_path=''):
    return render(request, 'main/404.html', status=404)
