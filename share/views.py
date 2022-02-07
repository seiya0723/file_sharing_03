from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages

from .models import Document,Review
from .forms import DocumentForm,ReviewForm

import magic
ALLOWED_MIME = ["image/jpeg", "application/zip", "video/mp4", "application/pdf"]


#CHECK:LoginRequiredMixinをViewと一緒に継承する(多重継承)することで、未認証のユーザーをログインページにリダイレクトすることができる。
class IndexView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):

        #ページネーションと検索機能


        #messages.info(request, "Hello world.")

        documents = Document.objects.all()
        context = {"documents":documents}

        return render(request,"share/index.html", context)

    def post(self, request, *args, **kwargs):

        #アップロードファイルが存在しない場合、リダイレクト。
        #想定外の処理をされた場合、return文を実行する。これをアーリーリターン(early return)。
        #メリット:ネストが深くなるのを防ぐ、処理速度が若干速くなる。

        if "content" not in request.FILES:
            messages.error(request, "ファイルがありません")
            return redirect("dojo:index")

        #mimeの取得、mimeをセットしたリクエストをバリデーションする。
        mime    = magic.from_buffer(request.FILES["content"].read(1024), mime=True)

        #TIPS:クライアントから受け取ったリクエストを直接書き換えすることはできない。そのためcopyメソッドでリクエストのコピーを作る。
        copied          = request.POST.copy()
        copied["mime"]  = mime

        #TODO:ユーザーIDをコピーしたリクエストに格納する。その上でバリデーション。
        copied["user"]  = request.user.id


        form = DocumentForm(copied, request.FILES)

        if form.is_valid():
            print("バリデーションOK")
            # 保存する

            if mime in ALLOWED_MIME:
                messages.success(request, "保存に成功しました")
                form.save()
            else:
                messages.error(request, "このファイルは許可されていません")
                print("このファイルは許可されていません")
        else:
            messages.error(request, form.errors)
            print(form.errors)
            print("バリデーションNG")
            print(mime)

        return redirect("share:index")

index   = IndexView.as_view()



#投稿されたファイルの個別ページ
class SingleView(View):

    #urls.pyに書かれたpkを引数として受け取り、ファイルを特定する。
    def get(self, request, pk, *args, **kwargs):

        context             = {}
        context["document"] = Document.objects.filter(id=pk).first()
        context["reviews"]  = Review.objects.filter(document=pk).order_by("-dt")

        return render(request,"share/single.html", context)

    def post(self, request, pk, *args, **kwargs):

        #TODO:ここで投稿されたファイルに対するレビューを受け付ける。
        pass

single  = Single.as_view()

